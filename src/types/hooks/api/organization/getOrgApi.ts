import { ComputedRef, Ref } from "vue";
import { OrganizationSchema } from "@/types";

/**
 * A hook for calling get organization API endpoints.
 */
export interface GetOrgApiHook {
  /**
   * Whether the get organization request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * All organizations for the current user.
   */
  allOrgs: Ref<OrganizationSchema[]>;
  /**
   * All organizations for the current user except the current organization.
   */
  unloadedOrgs: ComputedRef<OrganizationSchema[]>;
  /**
   * Adds or replaces an organization in the organization list.
   *
   * @param organization - The organization to add.
   */
  addOrg(organization: OrganizationSchema): void;
  /**
   * Removes an organization in the organization list.
   *
   * @param organization - The organization to remove.
   */
  removeOrg(organization: OrganizationSchema): void;
  /**
   * Switches to loading the given organization.
   *
   * @param organization - The organization to switch to.
   */
  handleSwitch(organization: OrganizationSchema): void;
  /**
   * Loads the current organization.
   */
  handleLoadCurrent(): Promise<void>;
}
