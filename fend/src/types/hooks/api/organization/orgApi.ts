import { ComputedRef, WritableComputedRef } from "vue";
import { IOHandlerCallback, OrganizationSchema } from "@/types";

/**
 * A hook for calling organization API endpoints.
 */
export interface OrgApiHook {
  /**
   * The current selected organization.
   * @reactive Updates stores and loads related data.
   */
  currentOrg: WritableComputedRef<OrganizationSchema>;
  /**
   * Whether the save organization request is loading.
   */
  saveOrgApiLoading: ComputedRef<boolean>;
  /**
   * Whether the delete organization request is loading.
   */
  deleteOrgApiLoading: ComputedRef<boolean>;
  /**
   * Creates a new organization, or updates an existing one.
   *
   * @param org - The organization to save.
   * @param callbacks - The callbacks to call after the action.
   */
  handleSave(
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
