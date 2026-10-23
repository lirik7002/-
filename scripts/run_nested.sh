#!/usr/bin/env bash
set -euo pipefail
python -m src.main --vfs vfs_samples/nested.xml --script starter_script.txt --debug
