import { defineStore } from "pinia";

import {
  IdentifierSchema,
  PermissionType,
  TeamSchema,
  OrganizationSchema,
} from "@/types";
import { roleMap } from "@/util";
import { projectStore, sessionStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This module manages user permissions.
 */
export const usePermission = defineStore("permissionStore", {
  state() {
    return {
      /**
       * Whether the app is in demo mode.
       */
      isDemo: false,
    };
  },
  actions: {
    /**
     * Checks whether the current user has the given permission.
     *
     * @param permission - The permission to check.
     * @param context - The context to check, be it a project, team, or organization.
     * @return Whether the current user has the requested permission.
     */
    isAllowed(
      permission: PermissionType,
      context:
        | IdentifierSchema
        | TeamSchema
        | OrganizationSchema = projectStore.project
    ): boolean {
      const member = sessionStore.getCurrentMember(context);
      const type = member?.entityType || "PROJECT";

      if (this.isDemo) {
        return false;
      } else if (permission === "safa.view") {
        return true;
      } else if (permission.startsWith("safa.")) {
        return !!sessionStore.user.superuser;
      }

      return !!member && roleMap[type][member.role].includes(permission);
    },
  },
});

export default usePermission(pinia);
