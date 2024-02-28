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

# Architecture

## Endpoints

Endpoints are defined by decorating the function with `@endpoint` which defines the serializer and whether it is a
celery task. Then, the function is registered under `api/server/urls`.

### `@endpoint`

The endpoint decorator will wrap a function so that:

1. Serialization is automatically handled
2. Documentation for endpoint is automatically created
3. If celery tasks, then execution is wrapped in task and task ID returned.

**AsyncEndpointHandler**
Defines the how asyncronous endpoints are handled including wrapping the function in a celery task.
**SyncEndpointHandler**
Defines syncronous endpoint containing base serialization functionality.