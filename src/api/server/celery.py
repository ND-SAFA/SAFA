import os

from celery import Celery
from dotenv import load_dotenv

from .paths import load_source_code_paths

load_source_code_paths()
load_dotenv()
CELERY_BROKER_URL = os.environ.get("BROKER_URL", "")  # collect_static.py runs through each file without env
celery = Celery('server',
                broker=CELERY_BROKER_URL,
                backend=CELERY_BROKER_URL)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
celery.autodiscover_tasks()
