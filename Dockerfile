# Flenuc Sky — single service for Cloud Run
# Build from repo root: docker build -t flenuc-sky .
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    ENV=production

WORKDIR /app

# System deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY apps/portfolio/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# App package + legal sources (primary packages/legal + bundled app/legal_md)
COPY apps/portfolio/app /app/app
COPY packages/legal /app/packages/legal

# Make packages/legal discoverable relative to repo-style layout used in config
# config.REPO_ROOT = PACKAGE_ROOT.parent.parent; with PACKAGE_ROOT=/app we map:
#   /app = apps/portfolio equivalent → parent.parent would be wrong.
# Override via env LEDGER_PATH; for legal, code falls back to app/legal_md.
ENV PYTHONPATH=/app \
    ENV=production \
    LEDGER_PATH=/tmp/flenuc-sky-ledger.json

# Non-root user
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

# Cloud Run sets PORT; default 8080
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
