#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

TGEN_PATH = os.path.join(os.path.dirname(__file__), "..", "tgen")

TGEN_PATH = os.path.normpath(TGEN_PATH)
sys.path.append(TGEN_PATH)
sys.path.append(os.path.join(TGEN_PATH, "tgen"))

print(TGEN_PATH)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
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
    main()
