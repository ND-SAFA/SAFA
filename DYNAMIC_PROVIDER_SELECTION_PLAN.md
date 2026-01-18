# Dynamic Provider Selection Implementation Plan

## Overview

This document outlines the changes needed to allow users to select their preferred AI provider (OpenAI or Anthropic) and have the system dynamically route requests to the selected provider using the user's API keys.

## Current State

The current implementation:
- Stores both OpenAI and Anthropic API keys for users
- Sends both keys to gen-api with every request
- gen-api uses a fallback pattern: request key → environment key
- Provider selection is hardcoded per endpoint/agent (not user-configurable)

## Desired State

The new implementation will:
- Allow users to select their preferred provider per request or as a default preference
- Store provider preference alongside API keys
- Send provider preference and corresponding API key to gen-api
- gen-api dynamically selects the appropriate LLM manager based on user preference
- Support per-request overrides of the default provider

---

## Architecture Changes

### 1. Database Layer (bend)

#### 1.1 Update `user_api_keys` Table Schema

**File**: `bend/src/main/resources/db/migration/V41_0__add_provider_preference.sql`

```sql
-- Add preferred provider column to user_api_keys table
ALTER TABLE user_api_keys
ADD COLUMN preferred_provider VARCHAR(50) DEFAULT 'openai';

-- Add check constraint to ensure valid provider values
ALTER TABLE user_api_keys
ADD CONSTRAINT chk_preferred_provider
CHECK (preferred_provider IN ('openai', 'anthropic'));

-- Add index for performance
CREATE INDEX idx_user_api_keys_provider ON user_api_keys(preferred_provider);
```

#### 1.2 Update `UserApiKey` Entity

**File**: `bend/src/main/java/edu/nd/crc/safa/features/users/entities/db/UserApiKey.java`

```java
@Entity
@Table(name = "user_api_keys")
public class UserApiKey implements Serializable {
    // ... existing fields ...

    @Column(name = "preferred_provider", length = 50)
    private String preferredProvider = "openai"; // Default to OpenAI

    // Add getter/setter
    public String getPreferredProvider() {
        return preferredProvider;
    }

    public void setPreferredProvider(String preferredProvider) {
        this.preferredProvider = preferredProvider;
    }
}
```

#### 1.3 Create Provider Enum

**File**: `bend/src/main/java/edu/nd/crc/safa/features/users/entities/enums/LLMProvider.java`

```java
package edu.nd.crc.safa.features.users.entities.enums;

public enum LLMProvider {
    OPENAI("openai", "OpenAI"),
    ANTHROPIC("anthropic", "Anthropic");

    private final String value;
    private final String displayName;

    LLMProvider(String value, String displayName) {
        this.value = value;
        this.displayName = displayName;
    }

    public String getValue() {
        return value;
    }

    public String getDisplayName() {
        return displayName;
    }

    public static LLMProvider fromValue(String value) {
        for (LLMProvider provider : values()) {
            if (provider.value.equals(value)) {
                return provider;
            }
        }
        throw new IllegalArgumentException("Unknown provider: " + value);
    }
}
```

---

### 2. Backend API Layer (bend)

#### 2.1 Update Request/Response DTOs

**File**: `bend/src/main/java/edu/nd/crc/safa/features/users/entities/app/ApiKeysRequest.java`

```java
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class ApiKeysRequest {
    private String openaiApiKey;
    private String anthropicApiKey;
    private String preferredProvider; // NEW: Add provider preference
}
```

**File**: `bend/src/main/java/edu/nd/crc/safa/features/users/entities/app/ApiKeysResponse.java`

```java
@Data
@AllArgsConstructor
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class ApiKeysResponse {
    private String openaiApiKey;
    private String anthropicApiKey;
    private String preferredProvider; // NEW: Add provider preference
    private boolean hasKeys;
}
```

#### 2.2 Update `UserApiKeyService`

**File**: `bend/src/main/java/edu/nd/crc/safa/features/users/services/UserApiKeyService.java`

```java
@Service
@AllArgsConstructor
public class UserApiKeyService {
    // ... existing code ...

    /**
     * Save or update user's API keys and provider preference.
     */
    public void saveApiKeys(
        UUID userId,
        String openaiKey,
        String anthropicKey,
        String preferredProvider // NEW parameter
    ) {
        UserApiKey apiKey = repository.findByUserId(userId)
            .orElse(new UserApiKey());

        apiKey.setUser(userRepository.findById(userId)
            .orElseThrow(() -> new IllegalArgumentException("User not found")));

        // Update keys if provided
        if (openaiKey != null && !openaiKey.trim().isEmpty()) {
            apiKey.setOpenaiApiKey(encryptionService.encrypt(openaiKey));
        }
        if (anthropicKey != null && !anthropicKey.trim().isEmpty()) {
            apiKey.setAnthropicApiKey(encryptionService.encrypt(anthropicKey));
        }

        // Update provider preference
        if (preferredProvider != null && !preferredProvider.trim().isEmpty()) {
            apiKey.setPreferredProvider(preferredProvider);
        }

        repository.save(apiKey);
    }

    /**
     * Enhanced UserApiKeys class to include provider preference.
     */
    @Data
    @AllArgsConstructor
    public static class UserApiKeys {
        private final String openaiKey;
        private final String anthropicKey;
        private final String preferredProvider;
    }

    /**
     * Get user's API keys and provider preference.
     */
    public UserApiKeys getApiKeys(UUID userId) {
        return repository.findByUserId(userId)
            .map(key -> new UserApiKeys(
                key.getOpenaiApiKey() != null ?
                    encryptionService.decrypt(key.getOpenaiApiKey()) : null,
                key.getAnthropicApiKey() != null ?
                    encryptionService.decrypt(key.getAnthropicApiKey()) : null,
                key.getPreferredProvider()
            ))
            .orElse(new UserApiKeys(null, null, "openai"));
    }
}
```

#### 2.3 Update `UserApiKeyController`

**File**: `bend/src/main/java/edu/nd/crc/safa/features/users/controllers/UserApiKeyController.java`

```java
@RestController
@RequestMapping(AppRoutes.Accounts.API_KEYS)
@AllArgsConstructor
public class UserApiKeyController {

    @PostMapping
    public ResponseEntity<Void> saveApiKeys(@RequestBody ApiKeysRequest request) {
        SafaUser currentUser = userService.getCurrentUser();

        apiKeyService.saveApiKeys(
            currentUser.getUserId(),
            request.getOpenaiApiKey(),
            request.getAnthropicApiKey(),
            request.getPreferredProvider() // NEW: Pass provider preference
        );

        return ResponseEntity.ok().build();
    }

    @GetMapping
    public ResponseEntity<ApiKeysResponse> getApiKeys() {
        SafaUser currentUser = userService.getCurrentUser();
        UserApiKeys keys = apiKeyService.getApiKeys(currentUser.getUserId());

        ApiKeysResponse response = new ApiKeysResponse(
            UserApiKeyService.maskApiKey(keys.getOpenaiKey()),
            UserApiKeyService.maskApiKey(keys.getAnthropicKey()),
            keys.getPreferredProvider(), // NEW: Include provider preference
            apiKeyService.hasApiKeys(currentUser.getUserId())
        );

        return ResponseEntity.ok(response);
    }
}
```

#### 2.4 Update `GenApiPayloadWrapper`

**File**: `bend/src/main/java/edu/nd/crc/safa/features/generation/common/GenApiPayloadWrapper.java`

```java
@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenApiPayloadWrapper<T> {
    @JsonUnwrapped
    private T payload;

    private String openaiApiKey;
    private String anthropicApiKey;
    private String preferredProvider; // NEW: Add provider preference
}
```

#### 2.5 Update `GenApiController`

**File**: `bend/src/main/java/edu/nd/crc/safa/features/generation/api/GenApiController.java`

```java
@Service
@AllArgsConstructor
public class GenApiController {

    private Object wrapPayloadWithApiKeys(Object payload) {
        UUID userId = userService.getCurrentUser().getUserId();

        if (!apiKeyService.hasApiKeys(userId)) {
            return payload; // No user keys, use environment keys
        }

        UserApiKeys apiKeys = apiKeyService.getApiKeys(userId);

        return new GenApiPayloadWrapper<>(
            payload,
            apiKeys.getOpenaiKey(),
            apiKeys.getAnthropicKey(),
            apiKeys.getPreferredProvider() // NEW: Include provider preference
        );
    }
}
```

---

### 3. Gen-API Layer (Python/Django)

#### 3.1 Update API Key Context Manager

**File**: `gen-api/gen-common/gen_common/llm/api_key_context.py`

```python
from contextvars import ContextVar
from typing import Optional

# Context variables for per-request API keys and provider
_request_openai_key: ContextVar[Optional[str]] = ContextVar('request_openai_key', default=None)
_request_anthropic_key: ContextVar[Optional[str]] = ContextVar('request_anthropic_key', default=None)
_request_preferred_provider: ContextVar[Optional[str]] = ContextVar('request_preferred_provider', default=None)  # NEW

class ApiKeyContext:
    """Thread-safe context for per-request API keys and provider preference."""

    @staticmethod
    def set_openai_key(key: Optional[str]) -> None:
        _request_openai_key.set(key)

    @staticmethod
    def get_openai_key() -> Optional[str]:
        return _request_openai_key.get()

    @staticmethod
    def set_anthropic_key(key: Optional[str]) -> None:
        _request_anthropic_key.set(key)

    @staticmethod
    def get_anthropic_key() -> Optional[str]:
        return _request_anthropic_key.get()

    # NEW: Provider preference methods
    @staticmethod
    def set_preferred_provider(provider: Optional[str]) -> None:
        """Set the preferred provider for this request."""
        _request_preferred_provider.set(provider)

    @staticmethod
    def get_preferred_provider() -> Optional[str]:
        """Get the preferred provider for this request."""
        return _request_preferred_provider.get()

    @staticmethod
    def clear() -> None:
        """Clear all context variables."""
        _request_openai_key.set(None)
        _request_anthropic_key.set(None)
        _request_preferred_provider.set(None)  # NEW


def get_effective_api_key(request_key: Optional[str], fallback_key: Optional[str]) -> Optional[str]:
    """Get effective API key with fallback."""
    return request_key if request_key is not None else fallback_key
```

#### 3.2 Update Serializer Mixin

**File**: `gen-api/src/api/endpoints/gen/serializers/api_key_serializer_mixin.py`

```python
from rest_framework import serializers

class ApiKeySerializerMixin(serializers.Serializer):
    """Mixin to add optional API key fields and provider preference to serializers."""

    openai_api_key = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    anthropic_api_key = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    preferred_provider = serializers.CharField(required=False, allow_null=True, allow_blank=True)  # NEW
```

#### 3.3 Update Request Handler

**File**: `gen-api/src/api/endpoints/handler/ihandler.py`

```python
class IHandler(ABC):

    def handle_request(self, request: HttpRequest) -> JsonResponse:
        try:
            raw_data = json.loads(request.body)
            serializer = self._serializer_class(data=raw_data)

            if not serializer.is_valid():
                return JsonResponse({'error': serializer.errors}, status=400)

            serialized_data = serializer.validated_data

            # Set API key context for this request
            self._set_api_key_context(raw_data)

            try:
                response = self._request_handler(serialized_data)
                return JsonResponse(response, encoder=NpEncoder, safe=False)
            finally:
                # Always clear context after request
                ApiKeyContext.clear()

        except Exception as e:
            logger.exception("Error handling request")
            return JsonResponse({'error': str(e)}, status=500)

    def _set_api_key_context(self, raw_data: Dict) -> None:
        """Extract and set API keys and provider preference in context."""
        if raw_data.get('openai_api_key'):
            ApiKeyContext.set_openai_key(raw_data['openai_api_key'])
        if raw_data.get('anthropic_api_key'):
            ApiKeyContext.set_anthropic_key(raw_data['anthropic_api_key'])
        if raw_data.get('preferred_provider'):  # NEW
            ApiKeyContext.set_preferred_provider(raw_data['preferred_provider'])
```

#### 3.4 Create Provider Selection Logic

**File**: `gen-api/gen-common/gen_common/llm/provider_selector.py` (NEW FILE)

```python
from typing import Optional, Union
from enum import Enum

from gen_common.constants.environment_constants import OPEN_AI_KEY, ANTHROPIC_KEY
from gen_common.llm.api_key_context import ApiKeyContext, get_effective_api_key
from gen_common.llm.abstract_llm_manager import AbstractLLMManager


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
            provider = LLMProvider(preferred.lower())

            # Validate that the preferred provider has an available API key
            if ProviderSelector._has_valid_key(provider):
                return provider
            else:
                # Log warning that preferred provider has no valid key
                print(f"Warning: Preferred provider '{provider.value}' has no valid API key, falling back")

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
            effective_key = get_effective_api_key(request_key, OPEN_AI_KEY)
            return effective_key is not None and effective_key.strip() != ""
        elif provider == LLMProvider.ANTHROPIC:
            request_key = ApiKeyContext.get_anthropic_key()
            effective_key = get_effective_api_key(request_key, ANTHROPIC_KEY)
            return effective_key is not None and effective_key.strip() != ""

        return False

    @staticmethod
    def create_manager(provider: Optional[LLMProvider] = None) -> AbstractLLMManager:
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
```

#### 3.5 Update BaseAgent to Use Provider Selector

**File**: `gen-api/gen-common/gen_common/graph/agents/base_agent.py`

```python
from gen_common.llm.provider_selector import ProviderSelector, LLMProvider

class BaseAgent:

    def _get_llm_manager(
        self,
        llm_selected: Optional[SupportedLLMs] = None,
        model_args: Optional[Dict[str, Any]] = None
    ) -> AbstractLLMManager:
        """
        Get the appropriate LLM manager based on user's provider preference.

        Args:
            llm_selected: Optional LLM type override
            model_args: Optional model arguments

        Returns:
            Configured LLM manager instance
        """
        # If specific LLM requested, use it
        if llm_selected is not None:
            if llm_selected == SupportedLLMs.OPENAI:
                from gen_common.llm.open_ai_manager import OpenAIManager
                from gen_common.llm.args.open_ai_args import OpenAIArgs
                return OpenAIManager(OpenAIArgs(**(model_args or {})))
            elif llm_selected == SupportedLLMs.ANTHROPIC:
                from gen_common.llm.anthropic_manager import AnthropicManager
                from gen_common.llm.args.anthropic_args import AnthropicArgs
                return AnthropicManager(AnthropicArgs(**(model_args or {})))

        # Otherwise, use provider selector to choose based on user preference
        preferred_provider = ProviderSelector.get_preferred_provider()
        return ProviderSelector.create_manager(preferred_provider)
```

---

### 4. Frontend Layer (fend)

#### 4.1 Update Types

**File**: `fend/src/types/domain/authentication.ts`

```typescript
/**
 * Defines a user API keys model.
 */
export interface UserApiKeysSchema {
  /**
   * The user's OpenAI API key (masked on retrieval).
   */
  openaiApiKey?: string;
  /**
   * The user's Anthropic API key (masked on retrieval).
   */
  anthropicApiKey?: string;
  /**
   * The user's preferred LLM provider.
   */
  preferredProvider?: 'openai' | 'anthropic';
}

/**
 * LLM Provider options.
 */
export type LLMProvider = 'openai' | 'anthropic';

/**
 * LLM Provider display information.
 */
export interface LLMProviderOption {
  value: LLMProvider;
  label: string;
  description: string;
}
```

#### 4.2 Update API Keys Settings Component

**File**: `fend/src/components/account/save/ApiKeysSettings.vue`

```vue
<template>
  <panel-card title="API Keys">
    <typography
      el="p"
      value="Configure your personal API keys for OpenAI and Anthropic. These keys will be used for AI-powered generation tasks instead of shared organization keys."
    />
    <typography
      el="p"
      class="q-mb-md"
      value="Your API keys are encrypted and stored securely. Enter new keys to update, or leave blank to keep existing keys."
    />

    <!-- NEW: Provider Selection -->
    <div class="q-mb-md">
      <typography el="label" value="Preferred Provider" class="q-mb-sm" />
      <q-select
        v-model="selectedProvider"
        :options="providerOptions"
        option-value="value"
        option-label="label"
        emit-value
        map-options
        outlined
        dense
        data-cy="select-preferred-provider"
      >
        <template #option="scope">
          <q-item v-bind="scope.itemProps">
            <q-item-section>
              <q-item-label>{{ scope.opt.label }}</q-item-label>
              <q-item-label caption>{{ scope.opt.description }}</q-item-label>
            </q-item-section>
          </q-item>
        </template>
      </q-select>
      <typography
        el="p"
        class="q-mt-sm text-caption text-grey-7"
        value="This provider will be used by default for AI generation tasks. You must provide an API key for your selected provider."
      />
    </div>

    <text-input
      v-model="openaiKey"
      label="OpenAI API Key"
      placeholder="sk-..."
      type="password"
      data-cy="input-openai-key"
      :hint="selectedProvider === 'openai' ? 'Required for your selected provider' : 'Optional'"
    />

    <text-input
      v-model="anthropicKey"
      label="Anthropic API Key"
      placeholder="sk-ant-..."
      type="password"
      data-cy="input-anthropic-key"
      :hint="selectedProvider === 'anthropic' ? 'Required for your selected provider' : 'Optional'"
    />

    <template #actions>
      <text-button
        label="Save API Keys"
        :disabled="!isValid"
        :loading="userApiKeysStore.loading"
        outlined
        data-cy="button-save-api-keys"
        @click="handleSave"
      />
      <text-button
        v-if="hasExistingKeys"
        label="Delete API Keys"
        :loading="userApiKeysStore.loading"
        color="negative"
        outlined
        data-cy="button-delete-api-keys"
        @click="handleDelete"
      />
    </template>
  </panel-card>
</template>

<script lang="ts">
export default {
  name: "ApiKeysSettings",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { userApiKeysStore } from "@/hooks";
import { LLMProvider, LLMProviderOption } from "@/types";
import {
  Typography,
  PanelCard,
  TextButton,
  TextInput,
} from "@/components/common";

const openaiKey = ref("");
const anthropicKey = ref("");
const selectedProvider = ref<LLMProvider>("openai");

const providerOptions: LLMProviderOption[] = [
  {
    value: "openai",
    label: "OpenAI",
    description: "Use GPT-4 and other OpenAI models",
  },
  {
    value: "anthropic",
    label: "Anthropic",
    description: "Use Claude and other Anthropic models",
  },
];

const hasChanges = computed(
  () =>
    openaiKey.value ||
    anthropicKey.value ||
    selectedProvider.value !== (userApiKeysStore.apiKeys.preferredProvider || "openai")
);

const hasExistingKeys = computed(
  () =>
    userApiKeysStore.apiKeys.openaiApiKey ||
    userApiKeysStore.apiKeys.anthropicApiKey
);

// Validate that the selected provider has an API key
const isValid = computed(() => {
  if (!hasChanges.value) return false;

  // If selecting OpenAI, must have OpenAI key (either existing or new)
  if (selectedProvider.value === "openai") {
    return openaiKey.value || userApiKeysStore.apiKeys.openaiApiKey;
  }

  // If selecting Anthropic, must have Anthropic key (either existing or new)
  if (selectedProvider.value === "anthropic") {
    return anthropicKey.value || userApiKeysStore.apiKeys.anthropicApiKey;
  }

  return false;
});

onMounted(async () => {
  await userApiKeysStore.handleLoad();

  // Set initial provider selection
  selectedProvider.value = userApiKeysStore.apiKeys.preferredProvider || "openai";
});

async function handleSave(): Promise<void> {
  const apiKeys: Record<string, string> = {
    preferredProvider: selectedProvider.value,
  };

  if (openaiKey.value) {
    apiKeys.openaiApiKey = openaiKey.value;
  }
  if (anthropicKey.value) {
    apiKeys.anthropicApiKey = anthropicKey.value;
  }

  await userApiKeysStore.handleSave(apiKeys, {
    success: "Your API keys and provider preference have been saved securely.",
    error: "Unable to save your API keys.",
    onSuccess: () => {
      openaiKey.value = "";
      anthropicKey.value = "";
    },
  });
}

function handleDelete(): void {
  userApiKeysStore.handleDelete({
    success: "Your API keys have been deleted.",
    error: "Unable to delete your API keys.",
    onSuccess: () => {
      openaiKey.value = "";
      anthropicKey.value = "";
      selectedProvider.value = "openai";
    },
  });
}
</script>
```

---

## Implementation Steps

### Phase 1: Database and Backend (bend)
1. Create and run database migration to add `preferred_provider` column
2. Update `UserApiKey` entity to include provider preference
3. Create `LLMProvider` enum
4. Update DTOs (`ApiKeysRequest`, `ApiKeysResponse`)
5. Update `UserApiKeyService` to handle provider preference
6. Update `UserApiKeyController` endpoints
7. Update `GenApiPayloadWrapper` to include provider
8. Update `GenApiController` to send provider preference

### Phase 2: Gen-API Backend (Python)
1. Update `ApiKeyContext` to store provider preference
2. Update serializer mixin to include provider field
3. Update request handler (`IHandler`) to extract and set provider
4. Create `ProviderSelector` utility class
5. Update `BaseAgent` to use `ProviderSelector`
6. Test dynamic provider selection

### Phase 3: Frontend (fend)
1. Update TypeScript types for provider preference
2. Create provider selection UI in `ApiKeysSettings` component
3. Add validation to ensure selected provider has an API key
4. Update API calls to include provider preference
5. Add visual feedback for selected provider

### Phase 4: Testing
1. Unit tests for `ProviderSelector`
2. Integration tests for provider switching
3. E2E tests for user flow (select provider → save keys → generate content)
4. Test fallback behavior when preferred provider has no key
5. Test error handling for invalid provider selection

---

## Edge Cases and Considerations

### 1. Provider Key Validation
- **Issue**: User selects OpenAI but only has Anthropic key
- **Solution**: Frontend validation prevents saving invalid combination
- **Fallback**: Backend validates and returns error if mismatch

### 2. Missing API Keys
- **Issue**: User has provider preference but no API key
- **Solution**: System falls back to environment keys or first available provider
- **Logging**: Log warning when falling back from user preference

### 3. Per-Request Override
- **Enhancement**: Allow frontend to override provider per request
- **Implementation**: Add optional `provider_override` field to generation requests
- **Use Case**: User wants to compare outputs from different providers

### 4. Model Compatibility
- **Issue**: Some prompts may be optimized for specific providers
- **Solution**: Document model capabilities and limitations
- **Future**: Add prompt adaptation layer for cross-provider compatibility

### 5. Cost Tracking
- **Enhancement**: Track usage per provider for billing
- **Implementation**: Add provider field to job/generation records
- **Use Case**: Users can see cost breakdown by provider

### 6. Migration Strategy
- **Existing Users**: Default to "openai" for backward compatibility
- **New Users**: Prompt to select provider during onboarding
- **Communication**: Announce new feature with migration guide

---

## Future Enhancements

### 1. Multiple Profiles
Allow users to save multiple provider configurations:
- "Personal" profile with own keys
- "Work" profile with organization keys
- Quick switching between profiles

### 2. Model-Level Selection
Extend provider selection to specific models:
- OpenAI: GPT-4, GPT-4 Turbo, GPT-3.5
- Anthropic: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku

### 3. Automatic Provider Selection
Intelligent routing based on:
- Task type (coding, writing, analysis)
- Cost optimization
- Rate limit awareness
- Model capabilities

### 4. Provider Health Monitoring
- Track provider availability and latency
- Automatic failover to backup provider
- User notifications for provider issues

### 5. Cost Estimation
- Show estimated cost before generation
- Set spending limits per provider
- Alert when approaching limits

---

## API Contract Changes

### Backend → Gen-API Request Payload

**Before:**
```json
{
  "prompt": "...",
  "openai_api_key": "sk-...",
  "anthropic_api_key": "sk-ant-..."
}
```

**After:**
```json
{
  "prompt": "...",
  "openai_api_key": "sk-...",
  "anthropic_api_key": "sk-ant-...",
  "preferred_provider": "anthropic"
}
```

### Frontend → Backend Save Request

**Before:**
```json
{
  "openai_api_key": "sk-...",
  "anthropic_api_key": "sk-ant-..."
}
```

**After:**
```json
{
  "openai_api_key": "sk-...",
  "anthropic_api_key": "sk-ant-...",
  "preferred_provider": "anthropic"
}
```

### Backend → Frontend Get Response

**Before:**
```json
{
  "openai_api_key": "sk-...***",
  "anthropic_api_key": "sk-ant-...***",
  "has_keys": true
}
```

**After:**
```json
{
  "openai_api_key": "sk-...***",
  "anthropic_api_key": "sk-ant-...***",
  "preferred_provider": "anthropic",
  "has_keys": true
}
```

---

## Rollout Plan

### Week 1: Database and Backend Core
- Day 1-2: Database migration and entity updates
- Day 3-4: Service layer and API endpoints
- Day 5: Testing and documentation

### Week 2: Gen-API Integration
- Day 1-2: Provider selector implementation
- Day 3-4: Agent updates and integration testing
- Day 5: Performance testing and optimization

### Week 3: Frontend
- Day 1-2: UI component development
- Day 3-4: Integration with backend
- Day 5: E2E testing and polish

### Week 4: Testing and Deployment
- Day 1-3: Comprehensive testing (unit, integration, E2E)
- Day 4: Staging deployment and validation
- Day 5: Production deployment and monitoring

---

## Monitoring and Metrics

### Key Metrics to Track
1. **Provider Distribution**: Percentage of requests per provider
2. **Fallback Rate**: How often system falls back from user preference
3. **Error Rate**: Errors by provider
4. **Latency**: Response time by provider
5. **Cost**: API costs by provider and user

### Alerts
1. High fallback rate (>10%)
2. Provider-specific error spikes
3. Missing API key errors
4. Invalid provider selection attempts

---

## Documentation Updates Required

1. **User Guide**: How to configure provider preference
2. **API Documentation**: New request/response formats
3. **Admin Guide**: Managing provider defaults
4. **Developer Guide**: Extending to support new providers
5. **Migration Guide**: For existing users

---

## Conclusion

This implementation adds dynamic provider selection while maintaining backward compatibility. The architecture is extensible to support additional providers in the future. The phased approach allows for incremental development and testing, reducing risk during rollout.
