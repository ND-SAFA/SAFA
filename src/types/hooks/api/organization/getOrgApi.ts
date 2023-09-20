import { ComputedRef, WritableComputedRef } from "vue";
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
   * The current organization.
   * - Reactively loads organization and sets current organization and team.
   */
  currentOrg: WritableComputedRef<OrganizationSchema | undefined>;
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
