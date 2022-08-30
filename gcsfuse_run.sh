#!/usr/bin/env bash
set -eo pipefail

# Create mount directory for service
mkdir -p "$MNT_DIR"

echo "Mounting GCS Fuse."
# gcsfuse --foreground --debug_fuse --debug_fs --debug_gcs --debug_http "$BUCKET" "$MNT_DIR"
gcsfuse "$BUCKET" "$MNT_DIR"
echo "Mounting completed."

exec /app/venv/bin/python3 /app/src/manage.py runserver 0.0.0.0:80

# Exit immediately when one of the background processes terminate.
wait -n
