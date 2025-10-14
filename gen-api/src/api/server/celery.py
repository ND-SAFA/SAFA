import os

from celery import Celery
from dotenv import load_dotenv

from .paths import load_source_code_paths
from .settings import GEN_BROKER

load_source_code_paths()
load_dotenv()
CELERY_BROKER_URL = os.environ.get("BROKER_URL", "")
if GEN_BROKER == "celery":
    BROKER_USERNAME = os.environ.get("BROKER_USERNAME", "")
    BROKER_PASSWORD = os.environ.get("BROKER_PASSWORD", "")

    celery = Celery('server',
                    broker=CELERY_BROKER_URL,
                    broker_connection_retry_on_startup=True)
    celery.conf.broker_user = BROKER_USERNAME
    celery.conf.broker_password = BROKER_PASSWORD
elif GEN_BROKER == "redis":
    celery = Celery('server',
                    broker_connection_retry_on_startup=True,
                    broker=CELERY_BROKER_URL,
                    backend=CELERY_BROKER_URL)
else:
    raise Exception(f"Broker {GEN_BROKER} not one of `redis` or `celery`.")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
celery.autodiscover_tasks()
