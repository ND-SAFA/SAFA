## Step - Build Arguments
FROM amazonlinux:2 as base
SHELL ["/bin/bash", "-c"]

## Makes sure that submodule has been copied (temp fix)
COPY tgen/requirements.txt /app/tgen/

## Step - Install python (TODO: Replace version with variable)
RUN yum update -y && yum groupinstall -y "Development tools" &&  \
    yum install -y wget openssl-devel bzip2-devel libffi-devel xz-devel &&  \
    wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz &&  \
    tar xvf Python-3.9.9.tgz
RUN cd Python-3.9.9 && ./configure --enable-optimizations && make install
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py


## Step - Install TGEN requirements

ADD tgen/requirements/ /app/tgen/requirements/
RUN pip3 install -r /app/tgen/requirements.txt

## Step - Install API requirements
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

## Step - Copy source and build files
COPY /tgen/tgen/ /app/tgen/
COPY /src/api/ /app/api/

### Step - Collect static files
WORKDIR /app
RUN python3 api/manage.py collectstatic --noinput

### COPy

# Finalize
EXPOSE 80
WORKDIR /app
CMD ["gunicorn" ,"--bind", ":80","--env", "DJANGO_SETTINGS_MODULE=api.server.settings", "--workers", "4","--threads","4","--timeout","0", "api.server.wsgi"]
