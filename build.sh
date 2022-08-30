DOCKER_BUILDKIT=1 docker build --build-arg BUCKET=safa-tgen-models -t safa-tgen:latest . && docker container rm safa-tgen && docker run --privileged -p 4050:80 --name safa-tgen safa-tgen
