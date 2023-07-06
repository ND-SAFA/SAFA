#!/bin/bash
if [ $# -eq 0 ]; then
  echo "Error: Container name is required."
  echo "Usage: ./build.sh <container>"
  exit 1
fi

# Check if container 'tgen' exists
container_name=${1}
if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
    echo "Container $container_name exists. Deleting..."
    docker compose stop $container_name # stop current
    docker compose rm $container_name # delete old
    docker compose build $container_name # Re-build new
    exit -1;
fi

echo "Starting $container_name ..."
docker compose up $container_name
