from django.forms import NullBooleanField
from drf_yasg import openapi
from rest_framework.fields import *
from rest_framework.relations import HyperlinkedIdentityField, HyperlinkedRelatedField, PrimaryKeyRelatedField, SlugRelatedField

from api.endpoints.gen.serializers.artifact_serializer import CleanCharField

"""
Maps Django fields to OpenAPI fields used for documentation generation.
"""
TYPE_MAP = {
    IntegerField: openapi.TYPE_INTEGER,
    FloatField: openapi.TYPE_NUMBER,
    DecimalField: openapi.TYPE_NUMBER,
    DateTimeField: openapi.TYPE_STRING,
    DateField: openapi.TYPE_STRING,
    TimeField: openapi.TYPE_STRING,
    DurationField: openapi.TYPE_STRING,
    CleanCharField: openapi.TYPE_STRING,
    CharField: openapi.TYPE_STRING,
    EmailField: openapi.TYPE_STRING,
    URLField: openapi.TYPE_STRING,
    UUIDField: openapi.TYPE_STRING,
    BooleanField: openapi.TYPE_BOOLEAN,
    NullBooleanField: openapi.TYPE_BOOLEAN,
    ChoiceField: openapi.TYPE_STRING,
    MultipleChoiceField: openapi.TYPE_ARRAY,
    FileField: openapi.TYPE_STRING,
    ImageField: openapi.TYPE_STRING,
    ListField: openapi.TYPE_ARRAY,
    DictField: openapi.TYPE_OBJECT,
    HiddenField: openapi.TYPE_STRING,
    ModelField: openapi.TYPE_OBJECT,
    PrimaryKeyRelatedField: openapi.TYPE_INTEGER,
    SlugRelatedField: openapi.TYPE_STRING,
    HyperlinkedIdentityField: openapi.TYPE_STRING,
    HyperlinkedRelatedField: openapi.TYPE_STRING,
    SerializerMethodField: openapi.TYPE_STRING,
}
