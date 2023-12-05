import { ComputedRef, WritableComputedRef } from "vue";
import { MembershipSchema } from "@/types";

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
  /**
   * Enables the superuser status of a member.
   * - Must be a superuser yourself.
   * @param member - The member to toggle.
   */
  enableSuperuser(member: MembershipSchema): Promise<void>;
}
