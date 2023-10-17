import { ComputedRef } from "vue";
import {
  IdentifierSchema,
  IOHandlerCallback,
  MemberEntitySchema,
  MembershipSchema,
  OrganizationSchema,
  TeamSchema,
} from "@/types";

/**
 * A hook for calling member API endpoints.
 */
export interface MemberApiHook {
  /**
   * Whether a member request is loading.
   */
  loading: ComputedRef<boolean>;

  /**
   * Updates the stored members for a project, team, or organization.
   *
   * @param entity - The entity to load the members of.
   */
  handleReload(entity: MemberEntitySchema): Promise<void>;

  /**
   * Invites a user to a project, team, or organization.
   *
   * @param member - The member to invite.
   * @param callbacks - Callbacks for the request.
   */
  handleInvite(
    member: MembershipSchema,
    callbacks: IOHandlerCallback
  ): Promise<void>;

  /**
   * Updates the role of a member.
   *
   * @param member - The member to update the role of.
   * @param callbacks - Callbacks for the request.
   */
  handleSaveRole(
    member: MembershipSchema,
    callbacks: IOHandlerCallback
  ): Promise<void>;

  /**
   * Opens a confirmation modal to delete the given member.
   *
   * @param member - The member to delete.
   * @param context - The context to check, be it a project, team, or organization.
   */
  handleDelete(
    member: MembershipSchema,
    context?: IdentifierSchema | TeamSchema | OrganizationSchema
  ): void;
}
