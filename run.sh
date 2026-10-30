#!/usr/bin/env bash
# Start the virtual lab locally.
set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

.venv/bin/pip install -q -r requirements.txt
exec .venv/bin/streamlit run app.py "$@"
