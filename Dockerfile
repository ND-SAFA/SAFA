## Step - Build Arguments
FROM amazonlinux:2 as base
SHELL ["/bin/bash", "-c"]

## Step - Install WGET
RUN apt update

## Step - Install python
ARG PYTHON_VERSION=3.9
ARG BOTO3_VERSION=1.6.3
ARG BOTOCORE_VERSION=1.9.3
ARG APPUSER=app

RUN yum -y update &&\
    yum install -y shadow-utils findutils gcc sqlite-devel zlib-devel \
                   bzip2-devel openssl-devel readline-devel libffi-devel && \
    groupadd ${APPUSER} && useradd ${APPUSER} -g ${APPUSER} && \
    cd /usr/local/src && \
    curl -O https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xzf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && make && make altinstall && \
    rm -rf /usr/local/src/Python-${PYTHON_VERSION}* && \
    yum remove -y shadow-utils audit-libs libcap-ng && yum -y autoremove && \
    yum clean all

## Step - Install TGEN requirements
COPY tgen/requirements.txt /app/tgen/
ADD tgen/requirements/ /app/tgen/requirements/
RUN pip3 install -r /app/tgen/requirements.txt

## Step - Install API requirements
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

## Step - Copy source and build files
COPY /tgen/ /app/tgen/
COPY /api/ /app/api/

# Finalize
EXPOSE 80
WORKDIR /app/api/
CMD ["gunicorn" ,"--bind", ":80", "--workers", "1","--threads","8","--timeout","0", "server.wsgi"]