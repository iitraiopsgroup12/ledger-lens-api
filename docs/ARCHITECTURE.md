# LedgerLens.ai Platform API — Service Documentation

The LedgerLens API is a **thin authentication / authorization proxy** built with
FastAPI. It sits in front of two in-cluster backends — **ledger-lens-sync** (system
of record) and **ledger-lens-rag** (RAG / LLM pipeline) — and is responsible for
authenticating callers, issuing and verifying JWTs, managing (stateless) sessions,
and forwarding each REST endpoint to the correct backend.

```
REST Clients  ──▶  LedgerLens API Proxy (FastAPI / Uvicorn, /api/v1)  ──▶  Backend services
                   • authenticate request                                  • ledger-lens-sync
                   • issue / verify JWT                                     • ledger-lens-rag
                   • stateless sessions
                   • forward each endpoint
```

> A visual companion to this document lives in [`architecture.drawio`](./architecture.drawio)
> (open with [diagrams.net](https://app.diagrams.net) or the VS Code Draw.io extension).

Run locally:

```bash
uv sync                                                  # install deps into .venv
uv run uvicorn app.main:app --reload --port 8001         # API at http://127.0.0.1:8001
#  docs:   http://127.0.0.1:8001/docs
#  health: http://127.0.0.1:8001/healthz
```

---

## 1 · Authentication, JWT issuance & session management

The proxy holds **no user store of its own**. Credentials and roles live in
ledger-lens-sync's `/users` resource; this service only verifies them and mints the
token that identifies the caller on every subsequent request.

### Login (the only unauthenticated route)

`POST /api/v1/auth/login` → `SyncAuthService.login()` (`app/services/auth_service.py`):

1. Look the user up by email via the Sync backend: `GET /users/email/{email_address}`
   (returns the stored bcrypt `password_hash`).
2. Verify the supplied password against that hash with `bcrypt.checkpw`
   (`verify_password` in `app/core/security.py`). A missing user and a wrong password
   both return a generic `401` so the response never discloses whether an email exists.
3. On success, mint a signed JWT (`create_access_token`) and return a `LoginResponse`
   containing the `access_token` and a minimal `{id, name}` user object.

### JWT structure

Signed in `app/core/security.py` with **HS256** (`JWT_ALGORITHM`) using `JWT_SECRET`:

| Claim   | Meaning                                  |
|---------|------------------------------------------|
| `sub`   | user id                                  |
| `email` | user email                               |
| `role`  | `admin` / regular user (drives RBAC)     |
| `name`  | display name                             |
| `iat`   | issued-at timestamp                      |
| `exp`   | expiry (`iat` + `JWT_EXPIRY_HOURS`, 24h) |

### Verifying requests & RBAC

Every other route depends on the auth dependencies in `app/api/deps.py`:

- **`get_current_user`** — `HTTPBearer` extracts the `Authorization: Bearer <jwt>`
  token; `decode_access_token` checks the signature and expiry and returns a
  `UserProfile`. A missing, expired, or tampered token yields `401`. **No upstream
  call is made on verification** — the token alone carries the identity.
- **`require_admin`** — builds on `get_current_user` and returns `403` unless
  `role == "admin"` (used by the `/scheduler` routes).

### Session model — stateless

There is **no server-side session store**. The identity lives entirely in the signed
JWT, which the client re-presents on each call. "Managing the session" therefore means
issuing the token at login, validating its signature/expiry on every request, and
letting it lapse after the 24-hour `exp`. Because all sharing of identity is via the
token, the proxy scales horizontally without sticky sessions.

> Configuration: `JWT_SECRET` **must** be overridden in every non-local environment;
> the default in `app/core/config.py` is for local development only.

---

## 2 · REST endpoints — forwarding to the RAG or Sync service

The app (`app/main.py`) mounts `api_router` under `/api/v1`. Each resource is one
router module under `app/api/v1/`, wired to a service via constructor-free DI in
`app/api/deps.py`. Routers are pure transport: they call the service and let
`ServiceError` subclasses propagate to the global handler.

| Endpoint(s)                                                        | Router            | Service (deps.py)          | Forwards to        |
|--------------------------------------------------------------------|-------------------|----------------------------|--------------------|
| `POST /auth/login`, `GET /auth/profile`                            | `auth`            | `SyncAuthService`          | **Sync**           |
| `GET /watchlist` (+ CRUD)                                          | `watchlist`       | `SyncWatchlistService`     | **Sync**           |
| `GET /companies/{symbol}/documents`, `GET /documents/{id}`, `…/download` | `documents` | `SyncDocumentService`      | **Sync**           |
| `GET /onboard`                                                     | `onboard`         | `SyncOnboardService`       | **Sync**           |
| `POST /analyst-reports`, `GET /companies/{symbol}/analyst-reports`, `…/sentiment` | `analyst_reports` | `SyncAnalystReportService` | **Sync** |
| `POST /chat`, `GET /chat/history`                                  | `chat`            | `RagChatService`           | **RAG**            |
| `POST /kpi/chat`, `POST /kpi/approve`                              | `kpi`             | `RagKpiService`            | **RAG**            |
| `GET /companies/search`, `GET /companies/{symbol}`                 | `companies`       | `InMemoryCompanyService`   | *in-memory (TODO)* |
| `GET /dashboard`                                                   | `dashboard`       | `InMemoryDashboardService` | *in-memory (TODO)* |
| `POST /scheduler/run`, `GET /scheduler/status` (admin)            | `scheduler`       | `InMemorySchedulerService` | *in-memory (TODO)* |

### Auth gating per router

- `auth` and `scheduler` declare their own auth: `auth/login` is open; `scheduler`
  routes require `require_admin`.
- All other routers attach `Depends(get_current_user)` at the router level, so every
  endpoint under them requires a valid JWT.

### Not yet forwarded

`companies`, `dashboard`, and `scheduler` are currently backed by `InMemory*Service`
placeholders that return seed data. They are wired the same way (swap the
implementation in `deps.py`) but do **not** yet call a backend — they are the
remaining integration work.

### Error mapping

`app/main.py` registers a global handler turning `ServiceError` subclasses into HTTP
responses: `AuthenticationError → 401`, `NotFoundError → 404`, `ConflictError → 409`,
`ProcessingError → 422`, anything else → `500`.

---

## 3 · The REST client and how it is mapped

Outbound calls to the backends go through typed HTTP clients in `app/clients/`, built
on a shared base.

### `BaseServiceClient` (`app/clients/base.py`)

- Wraps a single `httpx.Client(base_url, timeout)` (timeout defaults to **1800s / 30
  min** to match long RAG/KPI calls).
- Exposes one `request(method, path, **kwargs)` forwarding method.
- Translates upstream failures into the `ServiceError` hierarchy:
  `404 → NotFoundError`, `409 → ConflictError`, `422 → ProcessingError`, any other
  `≥400 → ProcessingError`, and connection errors → `ProcessingError`.
- Sends **no `Authorization` header** — the backends expose no auth scheme of their own;
  they are trusted in-cluster.

Two singletons are created in `deps.py` (`get_sync_client`, `get_rag_client`) from the
configured base URLs and shared by all services.

### `SyncServiceClient` → `ledger-lens-sync`

Maps proxy operations onto the Sync REST resources:

| Method group        | Upstream path(s)                                            |
|---------------------|------------------------------------------------------------|
| users               | `POST/GET/PATCH/DELETE /users`, `GET /users/{id}`, `GET /users/email/{email}` |
| companies           | `…/companies`                                              |
| watchlists          | `…/watchlists`                                             |
| documents           | `…/documents`                                              |
| chunks              | `…/chunks`                                                 |
| analyst reports     | `POST /analyst-reports` (multipart), `GET /analyst-reports`, `…/{id}` |
| update logs         | `…/update-logs`                                            |
| onboarding / health | `GET /onboard`, `GET /health`                              |

### `RagServiceClient` → `ledger-lens-rag`

| Method            | Upstream path                              |
|-------------------|--------------------------------------------|
| `ingest`          | `POST /api/v1/ingest` (JSON)               |
| `ingest_file`     | `POST /api/v1/ingest/file` (multipart)     |
| `query`           | `POST /api/v1/query` (JSON)                |
| `query_with_file` | `POST /api/v1/query-with-file` (multipart) |
| `kpi_chat`        | `POST /api/v1/kpi/chat` (form-urlencoded)  |
| `kpi_approve`     | `POST /api/v1/kpi/approve` (JSON)          |
| `health`          | `GET /api/v1/health`                       |

### Mapping chain

```
Router (transport)  →  <X>Service (business logic)  →  Sync/RagServiceClient  →  BaseServiceClient.request()  →  httpx  →  backend
                                                                                          │
                                                          upstream HTTP error  ───────────┘  →  ServiceError  →  global handler  →  HTTP status
```

Services are bound to **abstract interfaces** (`<X>Service(ABC)`) and resolved by the
`lru_cache`-memoized `get_*_service` providers, so routers depend on abstractions and a
real backend can be swapped in at a single point.

---

## 4 · Tools & technologies

### Language & tooling
- **Python ≥ 3.14** (pinned via `.python-version`)
- **uv** — dependency resolution and virtualenv management (`uv sync`, `uv run`)
- **python-dotenv** — loads configuration from `.env`

### Web / API framework
- **FastAPI** (`>=0.138.0`) — routing, dependency injection, automatic OpenAPI/Swagger
- **Uvicorn[standard]** — ASGI server (`timeout_keep_alive=1800` for long requests)
- **Pydantic[email]** (`>=2.13.4`) — request/response schemas and validation
- **python-multipart** — multipart/form-data parsing for file uploads
- **CORS middleware** — currently `allow_origins=["*"]`

### Authentication & security
- **PyJWT** — JWT signing & verification (HS256)
- **bcrypt** — password-hash verification
- **FastAPI `HTTPBearer`** — bearer-token extraction
- Stateless sessions — identity carried in the signed JWT, no session store

### Outbound HTTP
- **httpx** — synchronous HTTP client to the backends
- Typed `SyncServiceClient` / `RagServiceClient` over a shared `BaseServiceClient`
- 30-minute (1800s) request timeout

### Architecture & infrastructure
- **Clean architecture** — routers (transport) / services (logic) / clients (I/O) separated
- **Constructor-free DI** via `lru_cache` singleton providers in `app/api/deps.py`
- **Kubernetes** — backends reached by Service DNS (`http://ledger-lens-sync`,
  `http://ledger-lens-rag`)
- **OpenAPI spec-driven** — implemented from `docs/open-api-spec.json`
- Backend integrations (in the Sync/RAG services, not this proxy): Postgres / S3 /
  Pinecone / Gemini

### Configuration (environment variables)

| Variable                          | Default                       | Purpose                                  |
|-----------------------------------|-------------------------------|------------------------------------------|
| `LEDGER_LENS_SYNC_URL`            | `http://ledger-lens-sync`     | Sync backend base URL                    |
| `LEDGER_LENS_RAG_URL`             | `http://ledger-lens-rag`      | RAG backend base URL                     |
| `JWT_SECRET`                      | dev-only insecure default     | JWT signing secret (**override in prod**) |
| `JWT_ALGORITHM`                   | `HS256`                       | JWT signing algorithm                    |
| `JWT_EXPIRY_HOURS`               | `24`                          | Token lifetime                           |
| `BACKEND_REQUEST_TIMEOUT_SECONDS` | `1800`                        | Outbound httpx timeout                   |

---

## Project layout (reference)

```
app/
  main.py            # app init, CORS, ServiceError → HTTP handler, /healthz
  api/
    deps.py          # DI providers + get_current_user / require_admin
    v1/              # one router module per resource, aggregated in __init__.py
  core/
    config.py        # env-driven Settings
    security.py      # JWT issue/verify + bcrypt password check
  schemas/           # Pydantic models, one module per resource
  services/          # <X>Service(ABC) + concrete (Sync*/Rag*/InMemory*) impls
    exceptions.py    # ServiceError hierarchy
  clients/           # BaseServiceClient + Sync/Rag typed clients
docs/                # OpenAPI spec, backend specs, this doc, architecture.drawio
```