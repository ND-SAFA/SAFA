"""
Mixin for serializers that accept user-specific API keys.
"""

from rest_framework import serializers


class ApiKeySerializerMixin(serializers.Serializer):
    """
    Mixin that adds optional API key fields to serializers.
    These keys are used for per-request API authentication instead of global environment variables.
    """

    openai_api_key = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="OpenAI API key for this request (optional, falls back to environment if not provided)"
    )

    anthropic_api_key = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="Anthropic API key for this request (optional, falls back to environment if not provided)"
    )

    preferred_provider = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="Preferred LLM provider for this request (openai or anthropic)"
    )
