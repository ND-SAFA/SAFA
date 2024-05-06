#!/bin/bash

docker-compose build gen

# Check if the build was successful
if [ $? -eq 0 ]; then
  echo "Docker image build successful! Starting $container_name ..."

  # Run the Docker container
  docker-compose up --detach gen
  # docker run --env-file envs/.env -p 4000:80 -d --name $container_name --mount source=tgen-volume,destination=/vol --memory=8g $container_name
else
  echo "Docker image build failed!"
  exit 1
fi