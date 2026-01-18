<template>
  <panel-card title="API Keys">
    <typography
      el="p"
      value="Configure your personal API keys for AI-powered generation tasks. Select your preferred provider and enter the corresponding API key."
    />
    <typography
      el="p"
      class="q-mb-md"
      value="Your API keys are encrypted and stored securely. Enter new keys to update, or leave blank to keep existing keys."
    />

    <!-- Provider List -->
    <div class="providers-list">
      <div
        v-for="(provider, index) in providers"
        :key="provider.value"
        class="provider-item q-mb-md"
        :class="{ 'provider-selected': selectedProvider === provider.value }"
      >
        <div class="provider-header">
          <q-radio
            v-model="selectedProvider"
            :val="provider.value"
            :label="`${index + 1}. ${provider.label}`"
            :data-cy="`radio-provider-${provider.value}`"
            class="provider-radio"
          />
          <typography
            el="span"
            :value="provider.description"
            class="text-caption text-grey-7 q-ml-lg"
          />
        </div>

        <div class="provider-key-input q-mt-sm q-ml-lg">
          <text-input
            :model-value="getProviderKey(provider.value)"
            @update:model-value="(val) => setProviderKey(provider.value, val)"
            :label="`${provider.label} API Key`"
            :placeholder="provider.placeholder"
            type="password"
            :data-cy="`input-${provider.value}-key`"
            :hint="getKeyHint(provider.value)"
            outlined
            dense
          />
        </div>
      </div>
    </div>

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
/**
 * Allows users to manage their API keys and provider preference.
 */
export default {
  name: "ApiKeysSettings",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { userApiKeysStore } from "@/hooks";
import { LLMProvider } from "@/types";
import {
  Typography,
  PanelCard,
  TextButton,
  TextInput,
} from "@/components/common";

interface ProviderConfig {
  value: LLMProvider;
  label: string;
  description: string;
  placeholder: string;
}

const apiKeys = ref<Record<LLMProvider, string>>({
  openai: "",
  anthropic: "",
});

const selectedProvider = ref<LLMProvider>("openai");

const providers: ProviderConfig[] = [
  {
    value: "openai",
    label: "OpenAI",
    description: "Use GPT-4 and other OpenAI models",
    placeholder: "sk-...",
  },
  {
    value: "anthropic",
    label: "Anthropic",
    description: "Use Claude and other Anthropic models",
    placeholder: "sk-ant-...",
  },
];

const hasChanges = computed(() => {
  const hasKeyChanges = Object.values(apiKeys.value).some((key) => key);
  const hasProviderChange =
    selectedProvider.value !== (userApiKeysStore.apiKeys.preferredProvider || "openai");
  return hasKeyChanges || hasProviderChange;
});

const hasExistingKeys = computed(
  () =>
    userApiKeysStore.apiKeys.openaiApiKey ||
    userApiKeysStore.apiKeys.anthropicApiKey
);

// Validate that the selected provider has an API key
const isValid = computed(() => {
  if (!hasChanges.value) return false;

  // Check if the selected provider has either a new key or an existing key
  const provider = selectedProvider.value;
  const hasNewKey = apiKeys.value[provider];
  const hasExistingKey =
    provider === "openai"
      ? userApiKeysStore.apiKeys.openaiApiKey
      : userApiKeysStore.apiKeys.anthropicApiKey;

  return hasNewKey || hasExistingKey;
});

function getProviderKey(provider: LLMProvider): string {
  return apiKeys.value[provider];
}

function setProviderKey(provider: LLMProvider, value: string): void {
  apiKeys.value[provider] = value;
}

function getKeyHint(provider: LLMProvider): string {
  if (selectedProvider.value === provider) {
    return "Required for your selected provider";
  }
  return "Optional";
}

onMounted(async () => {
  await userApiKeysStore.handleLoad();

  // Set initial provider selection
  selectedProvider.value = userApiKeysStore.apiKeys.preferredProvider || "openai";
});

/**
 * Handles saving API keys and provider preference.
 */
async function handleSave(): Promise<void> {
  const payload: Record<string, string> = {
    preferredProvider: selectedProvider.value,
  };

  if (apiKeys.value.openai) {
    payload.openaiApiKey = apiKeys.value.openai;
  }
  if (apiKeys.value.anthropic) {
    payload.anthropicApiKey = apiKeys.value.anthropic;
  }

  await userApiKeysStore.handleSave(payload, {
    success: "Your API keys and provider preference have been saved securely.",
    error: "Unable to save your API keys.",
    onSuccess: () => {
      // Clear the input fields
      apiKeys.value.openai = "";
      apiKeys.value.anthropic = "";
    },
  });
}

/**
 * Handles deleting API keys.
 */
function handleDelete(): void {
  userApiKeysStore.handleDelete({
    success: "Your API keys have been deleted.",
    error: "Unable to delete your API keys.",
    onSuccess: () => {
      // Clear the input fields and reset to default provider
      apiKeys.value.openai = "";
      apiKeys.value.anthropic = "";
      selectedProvider.value = "openai";
    },
  });
}
</script>

<style scoped>
.providers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.provider-item {
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.provider-item:hover {
  border-color: #bdbdbd;
}

.provider-selected {
  border-color: #1976d2;
  background-color: #f5f9ff;
}

.provider-header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.provider-radio {
  font-weight: 500;
}

.provider-key-input {
  max-width: 600px;
}
</style>
