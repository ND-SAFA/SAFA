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
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

## Step - Copy source and build files
COPY gen-common/gen_common/ /app/gen_common/
COPY gen/gen/ /app/gen/
COPY src/api/ /app/api/

### COPy
ADD load.py /app/
COPY changelog /changelog

# Set safe environment variables
ENV DJANGO_SETTINGS_MODULE=api.server.settings \
    WANDB_MODE=offline \
    ENV_MODE=development

# Finalize
EXPOSE 80
WORKDIR /app
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]
