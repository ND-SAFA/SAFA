#!/bin/bash

# Start Celery worker in the background
python3 load.py
celery -A api.server worker --loglevel=info &
gunicorn --bind :80 --env DJANGO_SETTINGS_MODULE=api.server.settings --workers 4 --threads 4 --timeout 0 api.server.wsgi

# Optionally, you can add any additional commands or configuration here

# Script execution will halt until the Django server is stopped