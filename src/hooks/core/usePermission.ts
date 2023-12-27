import { defineStore } from "pinia";

import {
  IdentifierSchema,
  PermissionType,
  TeamSchema,
  OrganizationSchema,
  MembershipType,
} from "@/types";
import { projectStore, sessionStore, teamStore } from "@/hooks";
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
  getters: {
    /**
     * @return Whether the current user is a superuser.
     */
    isSuperuser(): boolean {
      return !!sessionStore.user.admin;
    },
  },
  actions: {
    /**
     * Returns the current context, be it a project, team, or organization.
     * @param type - The type of context to return.
     */
    getCurrentContext(
      type?: MembershipType
    ): IdentifierSchema | TeamSchema | OrganizationSchema {
      if (type === "TEAM") {
        return teamStore.team;
      } else if (type === "ORGANIZATION") {
        return teamStore.team;
      } else {
        return projectStore.project;
      }
    },
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
      if (this.isDemo) {
        return false;
      } else if (permission === "safa.view") {
        return true;
      } else if (permission.startsWith("safa.")) {
        return this.isSuperuser;
      } else {
        return context.permissions.includes(permission);
      }
    },
  },
});

export default usePermission(pinia);
