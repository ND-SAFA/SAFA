## Step - Build Arguments
FROM public.ecr.aws/docker/library/python:3.10 AS base
SHELL ["/bin/bash", "-c"]

# Install build dependencies for hdbscan on ARM64
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables for uv
ENV UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

## Step - Install requirements using uv
COPY requirements.txt /app/
RUN uv pip install --no-cache -r /app/requirements.txt

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
