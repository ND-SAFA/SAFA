# syntax=docker/dockerfile:1
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Step - Create VENV
WORKDIR /
RUN python3 -m venv $VIRTUAL_ENV

# Step - Install requirements
COPY requirements.txt /
RUN pip install -r requirements.txt

# Step - Copy code
COPY /src /src/

# Step - Start step
ENTRYPOINT ["python3",  "src/manage.py" ,"runserver" ,"0.0.0.0:5000"]