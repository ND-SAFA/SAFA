"""
Context manager for per-request API keys.

This module provides thread-safe context variables for managing user-specific API keys.
Each request can have its own OpenAI and Anthropic API keys, which are used instead of
global environment variables when available.
"""

from contextvars import ContextVar
from typing import Optional

# Thread-safe context variables for per-request API keys
_request_openai_key: ContextVar[Optional[str]] = ContextVar('request_openai_key', default=None)
_request_anthropic_key: ContextVar[Optional[str]] = ContextVar('request_anthropic_key', default=None)
_request_preferred_provider: ContextVar[Optional[str]] = ContextVar('request_preferred_provider', default=None)


class ApiKeyContext:
    """
    Manages per-request API keys using context variables.
    This allows different requests to use different API keys in a thread-safe manner.
    """

    @staticmethod
    def set_openai_key(key: Optional[str]) -> None:
        """Set OpenAI API key for current request context."""
        _request_openai_key.set(key)

    @staticmethod
    def set_anthropic_key(key: Optional[str]) -> None:
        """Set Anthropic API key for current request context."""
        _request_anthropic_key.set(key)

    @staticmethod
    def get_openai_key() -> Optional[str]:
        """Get OpenAI API key for current request context."""
        return _request_openai_key.get()

    @staticmethod
    def get_anthropic_key() -> Optional[str]:
        """Get Anthropic API key for current request context."""
        return _request_anthropic_key.get()

    @staticmethod
    def set_preferred_provider(provider: Optional[str]) -> None:
        """Set preferred LLM provider for current request context."""
        _request_preferred_provider.set(provider)

    @staticmethod
    def get_preferred_provider() -> Optional[str]:
        """Get preferred LLM provider for current request context."""
        return _request_preferred_provider.get()

    @staticmethod
    def clear() -> None:
        """Clear all API keys and preferences from current context."""
        _request_openai_key.set(None)
        _request_anthropic_key.set(None)
        _request_preferred_provider.set(None)


def get_effective_api_key(request_key: Optional[str], fallback_key: Optional[str]) -> Optional[str]:
    """
    Get the effective API key to use, preferring request-specific key over fallback.

    Args:
        request_key: API key from request context
        fallback_key: Global fallback API key from environment

    Returns:
        The API key to use, or None if neither is available
    """
    return request_key if request_key is not None else fallback_key
