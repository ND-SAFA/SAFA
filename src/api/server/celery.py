import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()
celery_app = None
if "BROKER_URL" in os.environ:
    BROKER_URL = os.environ["BROKER_URL"]
    BROKER_USERNAME = os.environ["BROKER_USERNAME"]
    BROKER_PASSWORD = os.environ["BROKER_PASSWORD"]

    celery_app = Celery('server',
                        broker=BROKER_URL)
    celery_app.conf.broker_user = BROKER_USERNAME
    celery_app.conf.broker_password = BROKER_PASSWORD

    # Using a string here means the worker doesn't have to serialize
    # the configuration object to child processes.
    # - namespace='CELERY' means all celery-related configuration keys
    #   should have a `CELERY_` prefix.
    celery_app.config_from_object('django.conf:settings', namespace='CELERY')

    # Load task modules from all registered Django apps.
    celery_app.autodiscover_tasks()
