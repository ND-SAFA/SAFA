import { defineStore } from "pinia";

import { computed } from "vue";
import { AdminApiHook, MembershipSchema } from "@/types";
import { ENABLED_FEATURES } from "@/util";
import { logStore, sessionStore } from "@/hooks";
import { activateSuperuser, createSuperuser, deactivateSuperuser } from "@/api";
import { pinia } from "@/plugins";
import useApi from "./useApi";

/**
 * This API store manages the current user's superuser status, allowing SAFA admins
 * to overrule permission checks.
 */
export const useAdminApi = defineStore("useAdmin", (): AdminApiHook => {
  const adminApi = useApi("adminApi");

  const displaySuperuser = computed(
    () => !!sessionStore.user?.admin || ENABLED_FEATURES.SUPERUSER_TEST
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

  async function enableSuperuser(member: MembershipSchema): Promise<void> {
    logStore.confirm(
      "Enable Superuser",
      `Are you sure you want to enable superuser for "${member.email}"?`,
      async (confirmed) => {
        if (!confirmed) return;

        await adminApi.handleRequest(async () => {
          await createSuperuser(member.email);
        });
      }
    );
  }

  return { displaySuperuser, activeSuperuser, enableSuperuser };
});

export default useAdminApi(pinia);
