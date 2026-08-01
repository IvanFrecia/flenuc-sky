#!/usr/bin/env bash
# Run portfolio app locally with uvicorn
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
APP_DIR="${ROOT}/apps/portfolio"
cd "${APP_DIR}"

if [[ ! -d .venv ]]; then
  if command -v uv >/dev/null 2>&1; then
    uv venv .venv
    # shellcheck disable=SC1091
    source .venv/bin/activate
    uv pip install -r requirements.txt
  else
    python3 -m venv .venv
    # shellcheck disable=SC1091
    source .venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
  fi
else
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

export PYTHONPATH="${APP_DIR}${PYTHONPATH:+:$PYTHONPATH}"
export PORT="${PORT:-8080}"
export ENV="${ENV:-development}"
export PUBLIC_BASE_URL="${PUBLIC_BASE_URL:-http://localhost:${PORT}}"

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}" --reload
