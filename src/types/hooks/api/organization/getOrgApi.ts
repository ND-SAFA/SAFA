import { ComputedRef } from "vue";

/**
 * A hook for calling get organization API endpoints.
 */
export interface GetOrgApiHook {
  /**
   * Whether the get organization request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * Loads the current organization.
   */
  handleLoadCurrent(): Promise<void>;
}
