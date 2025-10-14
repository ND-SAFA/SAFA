from typing import Dict

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

from api.docs.type_map import TYPE_MAP


def autodoc(serializer, *args, **kwargs):
    """
    Generates auto-schema from the fields in the serializer.
    :param serializer: The serializers whose properties are extracted.
    :param args: Positional args to swagger doc generator.
    :param kwargs: Keyword args to swagger doc generator.
    :return: The method being implemented (e.g. POST).
    """
    doc_info = create_serializer_swagger_info(serializer)
    return swagger_auto_schema(*args, **kwargs, **doc_info)


def create_serializer_swagger_info(serializer_class) -> Dict:
    """
    Creates swagger UI information for given serializer.
    :param serializer_class: The serializer class to document.
    :return: Returns the Swagger/OpenAPI schema information for a given serializer class.
    """
    fields = serializer_class().get_fields()
    properties = {}
    required = []

    for field_name, field in fields.items():
        properties[field_name] = get_schema_for_field(field)

        if field.required:
            required.append(field_name)

    return {
        'request_body': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=properties,
            required=required
        ),
        'responses': {
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=properties
                )
            ),
            400: "Bad Request"
        }
    }


def get_schema_for_field(field: serializers.Field):
    """
    Generates schema for field in serializer.
    :param field: The field to generate schema for.
    :return: The schema of the field.
    """
    if isinstance(field, serializers.Serializer):
        return create_serializer_swagger_info(field.__class__)['request_body']

    if field.help_text is None:
        parent_text = field.parent.help_text
        raise Exception(f"Child of `{parent_text}` is missing help text.")

    parent_fields = [serializers.ListField, serializers.ListSerializer, serializers.DictField]
    if any([isinstance(field, p) for p in parent_fields]):
        return openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=get_schema_for_field(field.child),
            description=field.help_text
        )

    else:
        schema_type = TYPE_MAP.get(field.__class__, None)
        if schema_type is None:
            raise AssertionError(f"Type not mapped to open API type: {field.__class__}")
        return openapi.Schema(
            type=schema_type,
            description=field.help_text
        )
