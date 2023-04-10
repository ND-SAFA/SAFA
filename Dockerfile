## Step - Build Arguments
ARG CUDA=11.7.1
ARG UBUNTU_VERSION=20.04
FROM nvidia/cuda:${CUDA}-base-ubuntu${UBUNTU_VERSION} as base
SHELL ["/bin/bash", "-c"]

## Step - Install WGET
RUN apt-get update

## Step - Install python
ARG PYTHON=python3.9
RUN apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y ${PYTHON} python3-pip && \
    rm -rf /var/lib/apt/lists/*

## Step - Install TGEN requirements
COPY tgen/requirements.txt /app/tgen/
RUN pip3 install -r /app/tgen/requirements.txt

## Step - Install API requirements
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

## Step - Copy source and build files
RUN apt-get git
RUN git submodule update --init --recursive
COPY /tgen/ /app/tgen/
COPY /api/ /app/api/

## Test
RUN python3

# Finalize
EXPOSE 80
WORKDIR /app/api/
CMD ["gunicorn" ,"--bind", ":80", "--workers", "1","--threads","8","--timeout","0", "server.wsgi"]