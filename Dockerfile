# syntax=docker/dockerfile:1.7

# ---- Stage 1: build the virtualenv with uv ---------------------------------
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

# uv tuning: copy deps into the venv (no symlinks across layers), don't try to
# download a different Python than the base image ships.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies first, using only the lockfiles, so this layer is cached
# until the dependency set actually changes.
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Now add the application source and install the project itself.
COPY app ./app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---- Stage 2: minimal runtime image ----------------------------------------
FROM python:3.14-slim-bookworm AS runtime

# Don't write .pyc files / buffer stdout; put the venv on PATH.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PORT=8001

# Run as an unprivileged user.
RUN groupadd --system app && useradd --system --gid app --home-dir /app app

WORKDIR /app

# Copy the resolved virtualenv and the application code from the builder.
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app app ./app

USER app

EXPOSE 8001

# Container-native healthcheck hitting the FastAPI /healthz endpoint.
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["python", "-c", "import os,urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8001')+'/healthz', timeout=3).status==200 else 1)"]

# Production server: bind all interfaces, no reload, and keep the long
# keep-alive that matches BACKEND_REQUEST_TIMEOUT_SECONDS (30 min) for slow
# RAG/KPI backend calls.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8001} --timeout-keep-alive 1800 --proxy-headers --forwarded-allow-ips '*'"]