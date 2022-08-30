# syntax=docker/dockerfile:1
FROM python:3.8-buster as base

# Sections
# ---
# 1. Build Arguments
# 2. Env Variables
# 3. Copy source + build files
# 4. Install librarires
# 5. Setup cloud file system
# 6. Run Commands

# 1. Build Arguments
ARG BUCKET

# 4. Install libraries
# Step - Install python libraries
COPY requirements.txt /app/
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install -r /app/requirements.txt

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

# 3. Copy source and build files
COPY /src /app/src/

# 2. Environment variables
ENV DEPLOYMENT_TYPE=local
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV BUCKET="$BUCKET"
ENV TRANSFORMERS_CACHE=/mnt/gcs/model-cache/
ENV MNT_DIR /mnt/gcs

# 5. Setup cloud file system
# ENV GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS:-/app/application-credentials.json}
# COPY application-credentials.json /app/
COPY gcsfuse_run.sh /app/
RUN chmod +x /app/gcsfuse_run.sh


# 6. Run commands
EXPOSE 80
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/app/gcsfuse_run.sh"]