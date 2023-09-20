import { defineStore } from "pinia";

import {
  IdentifierSchema,
  PermissionType,
  TeamSchema,
  OrganizationSchema,
  MembershipType,
} from "@/types";
import { roleMap } from "@/util";
import { orgStore, projectStore, sessionStore, teamStore } from "@/hooks";
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
      // TODO: use a project's team and organization instead of the current team and organization.
      const member = sessionStore.getCurrentMember(context);
      const teamMember = sessionStore.getCurrentMember(teamStore.team);
      const orgMember = sessionStore.getCurrentMember(orgStore.org);
      const type = member?.entityType || "PROJECT";

      if (this.isDemo) {
        return false;
      } else if (permission === "safa.view") {
        return true;
      } else if (permission.startsWith("safa.")) {
        return !!sessionStore.user.superuser;
      }

      return (
        (member && roleMap[type][member.role].includes(permission)) ||
        (teamMember && roleMap.TEAM[teamMember.role].includes(permission)) ||
        (orgMember &&
          roleMap.ORGANIZATION[orgMember.role].includes(permission)) ||
        false
      );
    },
  },
});

export default usePermission(pinia);
