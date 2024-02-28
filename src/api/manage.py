#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv

sys.path.append("/app/")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    try:

        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        from tgen.common.logging.logger_manager import logger

        env_file = sys.argv.pop(-1)
        env_file_path = os.path.normpath(os.path.join("..", "..", env_file))
        load_dotenv(env_file_path)
        logger.info(f"Loaded env {env_file}")
    PATH_TO_SRC = os.path.dirname(os.path.dirname(__file__))
    PATH_TO_TGEN = os.path.join(os.path.dirname(PATH_TO_SRC), "tgen")
    sys.path.append(PATH_TO_SRC)
    sys.path.append(PATH_TO_TGEN)
    main()
