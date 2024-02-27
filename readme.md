# Summary

Defines the API for generation jobs.

## Folder Structure

- src: API source code
    - api: Server code
        - cloud: Cloud API (e.g. Storage)
        - constants: Configuration used throughout project.
        - docs: Contains decorator that will automatically generate documentation based on the serializer provided.
        - endpoints: Code related to serializing and executing endpoints.
        - server: Django and Celery configuration files.
        - utils: Utility files used throughout project.
    - tests: Unit tests.
- tgen: TGEN as submodule