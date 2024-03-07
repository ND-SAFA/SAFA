## Step - Build Arguments
FROM public.ecr.aws/docker/library/python:3.9 as base
SHELL ["/bin/bash", "-c"]

RUN pip install --upgrade pip

## Step - Install requirements
COPY tgen/requirements.txt /app/tgen/
ADD tgen/requirements/ /app/tgen/requirements/
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt # file calls tgen requirements

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
