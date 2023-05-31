#!/bin/bash

# Check if container
container_name="bend"
if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
    echo "Container $container_name exists. Deleting..."
    docker stop $container_name
    docker rm $container_name
fi

# Re-build image
echo "Re-building '${container_name}' image..."
docker build -t $container_name .

## Run the newly built image
port=${1:-3000}
echo "Running the newly built '${container_name}' image..."
docker run --name $container_name -p $port:80 --env-file .env $container_name
