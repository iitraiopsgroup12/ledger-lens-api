# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current state

A hand-written (not openapi-generator-produced) FastAPI implementation, built from `docs/open-api-spec.json` per `docs/open-api-impl.instructions.md`. Requires Python `>=3.14` (see `.python-version`).

```bash
uv sync                                   # install deps into .venv
uv run uvicorn app.main:app --reload      # run the API; docs at /docs
```

There is no test suite or linter config configured yet.

## Architecture

Clean architecture: routers (transport) are decoupled from services (business logic) via constructor-free DI in `app/api/deps.py`.

- `app/main.py` — app init, mounts `api_router` under `/api/v1`, and a global `ServiceError` → HTTP status exception handler (`NotFoundError`→404, `ConflictError`→409, `ProcessingError`→422, anything else→500). Routers should let `ServiceError` subclasses propagate rather than catching them locally.
- `app/api/v1/` — one router module per resource (auth, companies, watchlist, documents, chat, analyst_reports, dashboard, scheduler), aggregated in `app/api/v1/__init__.py`.
- `app/api/deps.py` — `lru_cache`-memoized singleton providers (`get_*_service`) that return the abstract service interface type, plus `get_current_user`/`require_admin` auth dependencies.
- `app/schemas/` — Pydantic models, one module per resource, mirroring the `components.schemas` in `docs/open-api-spec.json`.
- `app/services/` — one `<X>Service(ABC)` interface + one `InMemory<X>Service` placeholder implementation per module. The in-memory implementations hold dummy/seed data only; swap them for real Postgres/S3/Pinecone/Gemini/MCP-backed classes as those integrations are built. `app/services/exceptions.py` defines the `ServiceError` hierarchy used for HTTP error mapping.

Auth is a placeholder: `get_current_user` in `deps.py` treats the bearer token as a raw user id rather than verifying a real JWT — see the `TODO` there and in `auth_service.py` before relying on it for anything beyond local development. Per `docs/API_Documentation.docx` section 5.4, real tokens should embed `user_id`/`role`/`exp` and only `POST /auth/login` should be unauthenticated.

## History worth knowing about

An earlier commit (`0c2167f`, "bootstrap LedgerLens API with OpenAPI contract and FastAPI skeleton") added a different, openapi-generator-produced FastAPI server under `generated-api/`. That generated tree was deleted in `aff8d9d` and the project was reset to a blank skeleton in `3cbae30` before the current hand-written implementation replaced it. `docs/API_Documentation.docx` (and the `docs/open-api-spec.json` derived from its section 4) is the authoritative source for this implementation, not the old generated tree.