#!/usr/bin/env bash
set -eo pipefail

# Create mount directory for service
mkdir -p "$MNT_DIR"

echo "Mounting GCS Fuse."
# gcsfuse --foreground --debug_fuse --debug_fs --debug_gcs --debug_http "$BUCKET" "$MNT_DIR"
gcsfuse --debug_fuse --debug_fs --debug_gcs --debug_http "$BUCKET" "$MNT_DIR"
echo "Mounting completed."

cd /app/src

exec gunicorn --bind :80 --workers 1 --threads 8 --timeout 0 server.wsgi &

# Exit immediately when one of the background processes terminate.
wait -n
