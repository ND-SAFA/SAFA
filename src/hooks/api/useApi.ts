import { defineStore } from "pinia";

import { ref, computed } from "vue";
import { IOHandlerCallback } from "@/types";
import { appStore, logStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * Creates a store for handling API requests.
 *
 * @param id - The unique store id to use.
 */
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
     * @param config - The success & error messages to display.
     * @param onSuccess - The callback to run on success.
     * @param onError - The callback to run on error.
     * @param onComplete - The callback to run on completion.
     */
    async function handleRequest<T = void>(
      cb: () => Promise<T>,
      { onSuccess, onError, onComplete }: IOHandlerCallback<T> = {},
      config: { success?: string; error?: string; useAppLoad?: boolean } = {}
    ): Promise<void> {
      loading.value = true;
      error.value = false;

      try {
        if (config.useAppLoad) {
          appStore.onLoadStart();
        }

        const res = await cb();

        onSuccess?.(res);

        if (config.success) {
          logStore.onSuccess(config.success);
        }
      } catch (e) {
        error.value = true;

        onError?.(e as Error);
        logStore.onDevError(String(e));

        if (config.error) {
          logStore.onError(config.error);
        }
      } finally {
        loading.value = false;

        if (config.useAppLoad) {
          appStore.onLoadEnd();
        }

        onComplete?.();
      }
    }

    return { loading, error, errorMessage, handleRequest, handleReset };
  });

export default (id: string) => useApi(id)(pinia);
