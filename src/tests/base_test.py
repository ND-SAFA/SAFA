import os
import uuid
from unittest import TestCase

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

from tgen.common.constants import anthropic_constants, environment_constants, open_ai_constants


class BaseTest(TestCase):
    """
    The common unit test for API layer.
    """

    def setUp(self) -> None:
        """
        Sets up the django environment.
        """
        load_dotenv()
        get_wsgi_application()
        environment_constants.IS_TEST = True
        open_ai_constants.OPENAI_MAX_ATTEMPTS = 1
        anthropic_constants.ANTHROPIC_MAX_RE_ATTEMPTS = 1
        os.environ["ANTHROPIC_API_KEY"] = str(uuid.uuid4())
