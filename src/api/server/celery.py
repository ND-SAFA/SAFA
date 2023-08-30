import os

from celery import Celery
from dotenv import load_dotenv

from .paths import load_paths

load_paths()
load_dotenv()

celery = None

if "BROKER_USERNAME" in os.environ:
    BROKER_USERNAME = os.environ["BROKER_USERNAME"]
    BROKER_PASSWORD = os.environ["BROKER_PASSWORD"]
    CELERY_BROKER_URL = os.environ["BROKER_URL"]

    celery = Celery('server',
                    broker=CELERY_BROKER_URL)
    celery.conf.broker_user = BROKER_USERNAME
    celery.conf.broker_password = BROKER_PASSWORD

    # Using a string here means the worker doesn't have to serialize
    # the configuration object to child processes.
    # - namespace='CELERY' means all celery-related configuration keys
    #   should have a `CELERY_` prefix.
    celery.config_from_object('django.conf:settings', namespace='CELERY')

    # Load task modules from all registered Django apps.
    celery.autodiscover_tasks()
