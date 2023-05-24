"""
WSGI config for api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.server.settings')

application = get_wsgi_application()

DIR_PATH = os.path.basename(__file__)
SRC_PATH = os.path.normpath(os.path.join(DIR_PATH, "..", "..", ".."))
sys.path.append(SRC_PATH)
