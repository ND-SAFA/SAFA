import { defineStore } from "pinia";

import { computed, ref } from "vue";
import { ApiHook, RequestConfig } from "@/types";
import { LOGOUT_ERROR } from "@/util";
import { appStore, logStore, sessionApiStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * Creates a store for handling API requests.
 *
 * @param id - The unique store id to use.
 */
export const useApi = (id: string) =>
  defineStore(`apiStore-${id}`, (): ApiHook => {
    const loading = ref(false);
    const error = ref(false);

    function handleReset(): void {
      loading.value = false;
      error.value = false;
    }

    function errorMessage(message: string) {
      return computed(() => (error.value ? message : false));
    }

    async function handleRequest<T = void>(
      cb: () => Promise<T>,
      config: RequestConfig<T> = {}
    ): Promise<T | undefined> {
      loading.value = true;
      error.value = false;

      try {
        if (config.useAppLoad) {
          appStore.onLoadStart();
        }

        const res = await cb();

        config.onSuccess?.(res);

        if (config.success) {
          logStore.onSuccess(config.success);
        }

        return res;
      } catch (e) {
        error.value = true;

        if ((e as Error)?.message === LOGOUT_ERROR) {
          // If the user's token has expired, log them out.
          await sessionApiStore.handleLogout();
          logStore.onWarning(LOGOUT_ERROR);
          return;
        }

        config.onError?.(e as Error);
        logStore.onDevError(String(e));

        if (config.error) {
          logStore.onError(config.error);
        }
      } finally {
        loading.value = false;

        if (config.useAppLoad) {
          appStore.onLoadEnd();
        }

        config.onComplete?.();
      }
    }

    return {
      loading,
      error,
      errorMessage,
      handleRequest,
      handleReset,
    };
  });

export default (id: string) => useApi(id)(pinia);
