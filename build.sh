#!/bin/bash

# Check if container 'tgen' exists
container_name="tgen"
if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
    echo "Container $container_name exists. Deleting..."
    docker stop $container_name
    docker rm $container_name
fi

# Re-build 'tgen' image
echo "Re-building 'tgen' image..."
docker build -t tgen .

## Run the newly built image
port=${1:-4000}
echo "Running the newly built 'tgen' image..."
docker run --name $container_name -p $port:80 --env-file .env $container_name