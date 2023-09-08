import { ComputedRef } from "vue";
import { IOHandlerCallback, OrganizationSchema } from "@/types";

/**
 * A hook for calling organization API endpoints.
 */
export interface OrgApiHook {
  /**
   * Whether the create organization request is loading.
   */
  createOrgApiLoading: ComputedRef<boolean>;
  /**
   * Whether the edit organization request is loading.
   */
  editOrgApiLoading: ComputedRef<boolean>;
  /**
   * Whether the delete organization request is loading.
   */
  deleteOrgApiLoading: ComputedRef<boolean>;
  /**
   * Creates a new organization.
   *
   * @param org - The organization to create.
   * @param callbacks - The callbacks to call after the action.
   */
  handleCreate(
    org: OrganizationSchema,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Edits the given organization.
   *
   * @param org - The organization to edit.
   * @param callbacks - The callbacks to call after the action.
   */
  handleEdit(
    org: OrganizationSchema,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Deletes the current organization.
   *
   * @param callbacks - The callbacks to call after the action.
   */
  handleDelete(callbacks?: IOHandlerCallback): Promise<void>;
}
