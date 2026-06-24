# LedgerLens.ai Platform API

FastAPI implementation of the LedgerLens.ai Platform API, generated from
[`docs/open-api-spec.json`](docs/open-api-spec.json) (derived from section 4
of `docs/API_Documentation.docx`).

## Setup

```bash
uv sync
```

## Run

```bash
uv run uvicorn app.main:app --reload --port 8001
```

API docs: http://127.0.0.1:8001/docs

## Architecture

- `app/api/v1/` — FastAPI routers (HTTP transport layer only)
- `app/api/deps.py` — dependency-injection providers for services and auth
- `app/schemas/` — Pydantic request/response models
- `app/services/` — business logic interfaces, each with a placeholder
  in-memory implementation. Swap the `InMemory*` classes for real
  Postgres/S3/Pinecone/Gemini/MCP-backed implementations as those
  integrations are built; routers depend only on the abstract interfaces.
