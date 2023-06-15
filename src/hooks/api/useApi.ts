import { defineStore } from "pinia";

import { ref, computed } from "vue";
import { IOHandlerCallback } from "@/types";
import { pinia } from "@/plugins";
import { logStore } from "@/hooks/core";

export const useApi = (id: string) =>
  defineStore(`apiStore-${id}`, () => {
    const loading = ref(false);
    const error = ref(false);

    /**
     * Resets the API state.
     */
    function handleReset(): void {
      loading.value = false;
      error.value = false;
    }

    /**
     * Creates a reactive error message for inputs.
     * @param message - The message to display.
     */
    function errorMessage(message: string) {
      return computed(() => (error.value ? message : false));
    }

    /**
     * Runs a request and handles the loading and error states,
     * as well as optionally reporting success and error messages.
     *
     * @param cb - The callback to run.
     * @param messages - The success & error messages to display.
     * @param onSuccess - The callback to run on success.
     * @param onError - The callback to run on error.
     * @param onComplete - The callback to run on completion.
     */
    async function handleRequest(
      cb: () => Promise<void>,
      { onSuccess, onError, onComplete }: IOHandlerCallback = {},
      messages: { success?: string; error?: string } = {}
    ): Promise<void> {
      loading.value = true;
      error.value = false;

      try {
        await cb();

        onSuccess?.();

        if (messages.success) {
          logStore.onSuccess(messages.success);
        }
      } catch (e) {
        error.value = true;

        onError?.(e as Error);
        logStore.onDevError(String(e));

        if (messages.error) {
          logStore.onError(messages.error);
        }
      } finally {
        loading.value = false;

        onComplete?.();
      }
    }

    return { loading, error, errorMessage, handleRequest, handleReset };
  });

export default (id: string) => useApi(id)(pinia);
