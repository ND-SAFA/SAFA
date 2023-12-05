import { ComputedRef, WritableComputedRef } from "vue";

/**
 * A hook for managing the admin API.
 */
export interface AdminApiHook {
  /**
   * Whether this user is a superuser.
   */
  displaySuperuser: ComputedRef<boolean>;
  /**
   * Whether this superuser's powers are active.
   * - Setting this value will update the user's superuser status.
   */
  activeSuperuser: WritableComputedRef<boolean>;
}
