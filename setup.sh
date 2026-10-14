#!/usr/bin/env bash
# Sets up a Python 3.12 virtual environment for hand_filter_cam.py.
#
# Why 3.12? MediaPipe (the hand-tracking library) does not ship wheels for
# the newest Python releases yet, so this pins to a version it supports.
set -euo pipefail

cd "$(dirname "$0")"

PY=python3.12
if ! command -v "$PY" >/dev/null 2>&1; then
    echo "python3.12 not found. Install it first, e.g.:"
    echo "    brew install python@3.12"
    exit 1
fi

"$PY" -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete. Run the app with:"
echo "    source .venv/bin/activate"
echo "    python hand_filter_cam.py"
