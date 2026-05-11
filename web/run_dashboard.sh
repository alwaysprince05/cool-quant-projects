#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
VENV="$ROOT/.venv"
if [[ ! -d "$VENV" ]]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install -q -r web/requirements.txt
PORT="${PORT:-8844}"
echo "Dashboard: http://127.0.0.1:${PORT}/"
exec "$VENV/bin/python" -m uvicorn web.app:app --host 127.0.0.1 --port "$PORT"
