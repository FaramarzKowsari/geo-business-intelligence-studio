#!/usr/bin/env sh
set -eu

[ -f .env ] || cp .env.example .env
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
exec uvicorn app.main:app --reload
