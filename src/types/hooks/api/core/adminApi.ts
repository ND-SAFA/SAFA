import { WritableComputedRef } from "vue";
import { MembershipSchema, OrganizationSchema, OrgPaymentTier } from "@/types";

/**
 * A hook for managing the admin API.
 */
export interface AdminApiHook {
  /**
   * Whether this superuser's powers are active.
   * - Setting this value will update the user's saved superuser status.
   */
  activeSuperuser: WritableComputedRef<boolean>;
  /**
   * Enables the superuser status of a member.
   * - Must be a superuser yourself.
   * @param member - The member to toggle.
   */
  enableSuperuser(member: Pick<MembershipSchema, "email">): Promise<void>;

  /**
   * Updates the payment tier of an organization.
   * @param org - The organization to update.
   * @param tier - The new payment tier.
   */
  updatePaymentTier(
    org: OrganizationSchema,
    tier: OrgPaymentTier
  ): Promise<void>;
}
