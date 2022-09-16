#!/usr/bin/env bash

gunicorn --bind :80 --workers 1 --threads 8 --timeout 0 server.wsgi &

# Exit immediately when one of the background processes terminate.
wait -n
