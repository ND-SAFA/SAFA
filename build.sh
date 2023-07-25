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
    docker compose rm -y $container_name # delete old
    docker compose build $container_name # Re-build new
fi

# Check if the build was successful
if [ $? -eq 0 ]; then
  echo "Docker image build successful! Starting $container_name ..."

  # Run the Docker container
  docker-compose --env-file .env up -d $container_name && echo "Docker container started!"
else
  echo "Docker image build failed!"
  exit 1
fi
