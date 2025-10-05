## Step - Build Arguments
FROM public.ecr.aws/docker/library/python:3.10 AS base
SHELL ["/bin/bash", "-c"]

# Install build dependencies for hdbscan on ARM64
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

## Step - Install requirements
ADD tgen/requirements/ /app/tgen/requirements/
RUN pip3 install -r /app/tgen/requirements/nlp-requirements.txt
RUN pip3 install -r /app/tgen/requirements/base-requirements.txt

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

# install task manager package.
ARG TASK_MANAGER=s3
COPY requirements/ /app/requirements
RUN pip3 install -r "/app/requirements/$TASK_MANAGER-requirements.txt"

## Step - Copy source and build files
COPY tgen/tgen/ /app/tgen/
COPY src/api/ /app/api/

### Step - Collect static files
WORKDIR /app
COPY tgen/download_static.py /app/download_static.py
RUN python3 download_static.py
RUN python3 api/manage.py collectstatic --noinput

### COPy
ADD load.py /app/
COPY changelog /changelog

# Finalize
EXPOSE 80
WORKDIR /app
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]
