from unittest import TestCase

from django.core.wsgi import get_wsgi_application


class ApiBaseTest(TestCase):
    """
    The common unit test for API layer.
    """

    def setUp(self) -> None:
        """
        Sets up the django environment.
        """
        get_wsgi_application()
