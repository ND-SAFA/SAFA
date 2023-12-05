import { defineStore } from "pinia";

import { computed } from "vue";
import { ENABLED_FEATURES } from "@/util";
import { sessionStore } from "@/hooks";
import { pinia } from "@/plugins";
import {
  activateSuperuser,
  deactivateSuperuser,
} from "@/api/endpoints/admin-api";
import { AdminApiHook } from "@/types/hooks/api/core/adminApi";
import useApi from "./useApi";

/**
 * This API store manages the current user's superuser status, allowing SAFA admins
 * to overrule permission checks.
 */
export const useAdminApi = defineStore("useAdmin", (): AdminApiHook => {
  const adminApi = useApi("adminApi");

  const displaySuperuser = computed(
    () => sessionStore.user?.superuser || ENABLED_FEATURES.SUPERUSER_TEST
  );

  const activeSuperuser = computed({
    get() {
      return sessionStore.user?.admin?.active || false;
    },
    set(value: boolean) {
      adminApi.handleRequest(async () => {
        if (value) {
          await activateSuperuser();
        } else {
          await deactivateSuperuser();
        }

        sessionStore.updateUser({ admin: { active: value } });
      });
    },
  });

  return { displaySuperuser, activeSuperuser };
});

export default useAdminApi(pinia);
