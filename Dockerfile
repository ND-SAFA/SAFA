## Step - Build Arguments
FROM python:3.9 as base
SHELL ["/bin/bash", "-c"]

## Step - Install TGEN requirements
COPY tgen/requirements.txt /app/tgen/
ADD tgen/requirements/ /app/tgen/requirements/
RUN pip3 install -r /app/tgen/requirements.txt

## Step - Install API requirements
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

## Step - Copy source and build files
COPY tgen/tgen/ /app/tgen/
COPY src/api/ /app/api/

### Step - Collect static files
WORKDIR /app
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
