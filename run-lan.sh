#!/usr/bin/env bash
# Start the virtual lab so other devices on the school Wi-Fi can open it.
set -e
cd "$(dirname "$0")"

IP=$(hostname -I 2>/dev/null | awk '{print $1}')
echo "Open http://${IP:-<this-computer-ip>}:8501 from any phone or laptop on the same network"
echo

exec ./run.sh --server.address 0.0.0.0 --server.port 8501
