# syntax=docker/dockerfile:1
# Steps
# ---
# 1. Install build tools (e.g. wget)
# 2. Install python and pip
# 3. Install requirements
# 4. Install librarires
# 5. Setup cloud file system
# 6. Run Commands

# Step - Build Arguments
# Options: https://hub.docker.com/r/nvidia/cuda
ARG CUDA=11.7.1
ARG UBUNTU_VERSION=20.04
FROM nvidia/cuda:${CUDA}-base-ubuntu${UBUNTU_VERSION} as base

# Step - Setup build tools
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
RUN apt-get install unzip

# Step - Install python
ARG PYTHON=python3.9
RUN apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y ${PYTHON} python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Step - Install python libraries
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

# Step - Install tini and gcsfuse
RUN set -e; \
    apt-get update -y && apt-get install -y \
    tini \
    lsb-release; \
    gcsFuseRepo=gcsfuse-`lsb_release -c -s`; \
    echo "deb http://packages.cloud.google.com/apt $gcsFuseRepo main" | \
    tee /etc/apt/sources.list.d/gcsfuse.list; \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    apt-key add -; \
    apt-get update; \
    apt-get install -y gcsfuse \
    && apt-get clean spo

# Step - Copy source and build files
COPY /src /app/src/

# Step - Environment variables
ENV DEPLOYMENT_TYPE=local
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV BUCKET=safa-tgen-models
ENV TRANSFORMERS_CACHE=/mnt/gcs/model-cache/
ENV MNT_DIR /mnt/gcs

# Step - Copy source and build files
WORKDIR /app/src
COPY /src .
ADD start.sh .
RUN chmod +x start.sh

# Step - LOCAL ONLY
# ENV GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS:-/app/application-credentials.json}
# COPY application-credentials.json /app/

# Step - Environment variables
ENV DEPLOYMENT_TYPE=local
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/model-cache/
ENV MNT_DIR=/tgen

# Step - Run commands
EXPOSE 80
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/app/src/start.sh"]