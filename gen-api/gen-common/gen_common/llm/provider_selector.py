"""
Provider selection logic for determining which LLM provider to use based on user preferences.
"""

from typing import Optional
from enum import Enum
import os

from gen_common.llm.api_key_context import ApiKeyContext, get_effective_api_key


class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class ProviderSelector:
    """
    Determines which LLM provider to use based on user preference and available API keys.
    """

    @staticmethod
    def get_preferred_provider() -> LLMProvider:
        """
        Get the preferred provider for the current request.

        Priority:
        1. User's preferred provider from request context
        2. First available provider with valid API key
        3. Default to OpenAI

        Returns:
            LLMProvider enum indicating which provider to use
        """
        # Check user preference from context
        preferred = ApiKeyContext.get_preferred_provider()

        if preferred:
            try:
                provider = LLMProvider(preferred.lower())

                # Validate that the preferred provider has an available API key
                if ProviderSelector._has_valid_key(provider):
                    return provider
                else:
                    # Log warning that preferred provider has no valid key
                    print(f"Warning: Preferred provider '{provider.value}' has no valid API key, falling back")
            except ValueError:
                print(f"Warning: Unknown provider '{preferred}', falling back to default")

        # Fallback: Check which providers have valid keys
        if ProviderSelector._has_valid_key(LLMProvider.OPENAI):
            return LLMProvider.OPENAI
        elif ProviderSelector._has_valid_key(LLMProvider.ANTHROPIC):
            return LLMProvider.ANTHROPIC

        # Default to OpenAI (will fail later if no key available)
        return LLMProvider.OPENAI

    @staticmethod
    def _has_valid_key(provider: LLMProvider) -> bool:
        """Check if the given provider has a valid API key available."""
        if provider == LLMProvider.OPENAI:
            request_key = ApiKeyContext.get_openai_key()
            fallback_key = os.environ.get('OPENAI_KEY')
            effective_key = get_effective_api_key(request_key, fallback_key)
            return effective_key is not None and effective_key.strip() != ""
        elif provider == LLMProvider.ANTHROPIC:
            request_key = ApiKeyContext.get_anthropic_key()
            fallback_key = os.environ.get('ANTHROPIC_KEY')
            effective_key = get_effective_api_key(request_key, fallback_key)
            return effective_key is not None and effective_key.strip() != ""

        return False

    @staticmethod
    def create_manager(provider: Optional[LLMProvider] = None):
        """
        Create the appropriate LLM manager based on provider preference.

        Args:
            provider: Optional provider override. If None, uses get_preferred_provider()

        Returns:
            Instance of OpenAIManager or AnthropicManager
        """
        from gen_common.llm.open_ai_manager import OpenAIManager
        from gen_common.llm.anthropic_manager import AnthropicManager
        from gen_common.llm.args.open_ai_args import OpenAIArgs
        from gen_common.llm.args.anthropic_args import AnthropicArgs

        if provider is None:
            provider = ProviderSelector.get_preferred_provider()

        if provider == LLMProvider.OPENAI:
            return OpenAIManager(OpenAIArgs())
        elif provider == LLMProvider.ANTHROPIC:
            return AnthropicManager(AnthropicArgs())
        else:
            raise ValueError(f"Unknown provider: {provider}")
