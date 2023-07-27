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
    docker stop $container_name # stop current
    docker rm -f $container_name # delete old
    docker build -t $container_name . # Re-build new
fi

# Check if the build was successful
if [ $? -eq 0 ]; then
  echo "Docker image build successful! Starting $container_name ..."

  # Run the Docker container
  docker run --env-file .env -p 4000:80 -d --name $container_name $container_name
else
  echo "Docker image build failed!"
  exit 1
fi