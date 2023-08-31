import { defineStore } from "pinia";

import {
  IdentifierSchema,
  OrganizationPermissionType,
  ProjectPermissionType,
  MemberRole,
} from "@/types";
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
      /**
       * A mapping from project permission types to project roles.
       */
      projectRoleMap: {
        viewer: [
          MemberRole.VIEWER,
          MemberRole.EDITOR,
          MemberRole.ADMIN,
          MemberRole.OWNER,
        ],
        editor: [MemberRole.EDITOR, MemberRole.ADMIN, MemberRole.OWNER],
        admin: [MemberRole.ADMIN, MemberRole.OWNER],
        owner: [MemberRole.OWNER],
      } as Record<ProjectPermissionType, MemberRole[]>,
    };
  },
  actions: {
    /**
     * Checks whether the current user has the given permission for their organization.
     *
     * @param permission - The permission to check.
     * @return Whether the current user has the requested permission.
     */
    organizationAllows(permission: OrganizationPermissionType): boolean {
      return permission !== "navigation" || !this.isDemo;
    },
    /**
     * Checks whether the current user has the given permission on the given project.
     *
     * @param permission - The permission to check.
     * @param project - The project to check.
     * @return Whether the current user has the requested permission.
     */
    projectAllows(
      permission: ProjectPermissionType,
      project: IdentifierSchema = projectStore.project
    ): boolean {
      const member = sessionStore.getProjectMember(project);

      return (
        this.organizationAllows("navigation") &&
        !!member &&
        this.projectRoleMap[permission].includes(member.role)
      );
    },
  },
});

export default usePermission(pinia);
