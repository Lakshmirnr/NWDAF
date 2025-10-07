#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=.
uvicorn app.main:app --host 0.0.0.0 --port 8088 --reload
