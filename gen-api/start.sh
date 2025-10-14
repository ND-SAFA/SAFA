#!/bin/bash

# Start Celery worker in the background
N_WORKERS=${N_WORKERS:-10}
python3 load.py
celery -A api.server worker --loglevel=info --concurrency=1 &
gunicorn --bind :80 --env DJANGO_SETTINGS_MODULE=api.server.settings --workers "$N_WORKERS" --threads 1 --timeout 0 api.server.wsgi

# Optionally, you can add any additional commands or configuration here

# Script execution will halt until the Django server is stopped