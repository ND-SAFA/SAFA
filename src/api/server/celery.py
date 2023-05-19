import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

BROKER_URL = os.environ["BROKER_URL"]
BROKER_USERNAME = os.environ["BROKER_USERNAME"]
BROKER_PASSWORD = os.environ["BROKER_PASSWORD"]

app = Celery('server',
             broker=BROKER_URL)
app.conf.broker_user = BROKER_USERNAME
app.conf.broker_password = BROKER_PASSWORD

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
