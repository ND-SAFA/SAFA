import { defineStore } from "pinia";
import { computed, ref, ComputedRef, Ref } from "vue";
import { UserApiKeysSchema, IOHandlerCallback } from "@/types";
import {
  getUserApiKeys,
  saveUserApiKeys,
  deleteUserApiKeys,
} from "@/api";
import { useApi } from "@/hooks/api/core/useApi";
import { pinia } from "@/plugins";

export interface UserApiKeysHook {
  loading: ComputedRef<boolean>;
  error: ComputedRef<boolean>;
  apiKeys: Ref<UserApiKeysSchema>;
  handleLoad: () => Promise<void>;
  handleSave: (
    apiKeys: UserApiKeysSchema,
    callbacks?: IOHandlerCallback
  ) => Promise<void>;
  handleDelete: (callbacks?: IOHandlerCallback) => Promise<void>;
  handleReset: () => void;
}

/**
 * A store for handling user API keys requests.
 */
export const useUserApiKeys = defineStore(
  "userApiKeys",
  (): UserApiKeysHook => {
    const apiKeysApi = useApi("userApiKeys")();
    const apiKeys = ref<UserApiKeysSchema>({});

    const loading = computed(() => apiKeysApi.loading);
    const error = computed(() => apiKeysApi.error);

    async function handleLoad(): Promise<void> {
      await apiKeysApi.handleRequest(async () => {
        apiKeys.value = await getUserApiKeys();
      });
    }

    async function handleSave(
      newApiKeys: UserApiKeysSchema,
      callbacks?: IOHandlerCallback
    ): Promise<void> {
      await apiKeysApi.handleRequest(async () => {
        await saveUserApiKeys(newApiKeys);
        apiKeys.value = newApiKeys;
      }, callbacks);
    }

    async function handleDelete(
      callbacks?: IOHandlerCallback
    ): Promise<void> {
      await apiKeysApi.handleRequest(async () => {
        await deleteUserApiKeys();
        apiKeys.value = {};
      }, callbacks);
    }

    function handleReset(): void {
      apiKeys.value = {};
      apiKeysApi.handleReset();
    }

    return {
      loading,
      error,
      apiKeys,
      handleLoad,
      handleSave,
      handleDelete,
      handleReset,
    };
  }
);

export default useUserApiKeys(pinia);
