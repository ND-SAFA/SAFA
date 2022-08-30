# syntax=docker/dockerfile:1
FROM python:3.8-buster as base

# Sections
# ---
# 1. Build Arguments
# 2. Env Variables
# 3. Copy source + build files
# 4. Install librarires
# 5. Copy google credentails if local run
# 6. Run Commands

# 2. Environment variables
ENV DEPLOYMENT_TYPE=local
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Copy source and build files
COPY /src /app/src/
COPY requirements.txt /app/

# 4. Install libraries
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install -r /app/requirements.txt

# 5. Uncomment for local builds
# TODO: Conditionally run these commands in deployment type is local
# ENV GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS:-/app/application-credentials.json}
# COPY application-credentials.json /app/


# 6. Run commands
EXPOSE 80
CMD [ "/app/venv/bin/python", "/app/src/manage.py", "runserver", "0.0.0.0:80"]