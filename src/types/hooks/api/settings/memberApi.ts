import { ComputedRef } from "vue";
import { IOHandlerCallback, MembershipSchema, ProjectRole } from "@/types";

/**
 * A hook for calling member API endpoints.
 */
export interface MemberApiHook {
  /**
   * Whether a member request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * Updates the current project's members.
   */
  handleReload(): Promise<void>;
  /**
   * Adds a user to a project and logs the status.
   *
   * @param projectId - The project to add this user to.
   * @param memberEmail - The email of the given user.
   * @param projectRole - The role to set for the given user.
   * @param callbacks - Callbacks for the request.
   */
  handleInvite(
    projectId: string,
    memberEmail: string,
    projectRole: ProjectRole,
    callbacks: IOHandlerCallback
  ): Promise<void>;
  /**
   * Updates the role of a member.
   *
   * @param projectId - The project to add this user to.
   * @param memberEmail - The email of the given user.
   * @param projectRole - The role to set for the given user.
   * @param callbacks - Callbacks for the request.
   */
  handleSaveRole(
    projectId: string,
    memberEmail: string,
    projectRole: ProjectRole,
    callbacks: IOHandlerCallback
  ): Promise<void>;
  /**
   * Opens a confirmation modal to delete the given member.
   *
   * @param member - The member to delete.
   */
  handleDelete(member: MembershipSchema): void;
}
