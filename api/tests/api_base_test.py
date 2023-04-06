import json
from typing import Dict
from unittest import TestCase

from celerytest import setup_celery_worker
from celerytest.testcase import CeleryTestCaseMixin
from django.core.wsgi import get_wsgi_application
from django.test import Client
from dotenv import load_dotenv

from server.celery import app

setup_celery_worker(app)  # need to setup worker outside


class ApiBaseTest(CeleryTestCaseMixin, TestCase):
    """
    The common unit test for API layer.
    """
    celery_app = app
    celery_concurrency = 4

    def setUp(self) -> None:
        """
        Sets up the django environment.
        """
        load_dotenv()
        get_wsgi_application()

    @staticmethod
    def request(url: str, data: Dict = None, method: str = "POST", content_type="application/json"):
        """
        Requests the application at given url
        :param url: The url to make request for.
        :param data: The data to include in request.
        :param method: The type of request to make.
        :param content_type: The type of content expected to be received.
        :return:
        """
        c = Client()
        methods = {
            "POST": c.post,
            "GET": c.get
        }
        assert method in methods, f"Expected method to be one of: {methods.keys()}"
        response = methods[method](url, data=data, content_type=content_type)
        if response.status_code >= 300:
            raise Exception(response.content)
        return json.loads(response.content)
