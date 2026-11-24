#!/bin/sh
# Start the API and the UI together on http://127.0.0.1:8088
cd "$(dirname "$0")" || exit 1
PY="${PYTHON:-../aeroguard/.venv/bin/python}"
export FINALDAY_SUPERVISOR_CODE="${FINALDAY_SUPERVISOR_CODE:-2468}"
exec "$PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8088
