import { WritableComputedRef } from "vue";
import { MembershipSchema, OrganizationSchema, OrgPaymentTier } from "@/types";

/**
 * A hook for managing the admin API.
 */
export interface AdminApiHook {
  /**
   * Whether this superuser's powers are active.
   *
   * @reactive Updates the user's saved superuser status.
   */
  activeSuperuser: WritableComputedRef<boolean>;
  /**
   * Enables the superuser status of a member.
   *
   * @assumption Must be a superuser.
   *
   * @param member - The member to toggle.
   */
  enableSuperuser(member: Pick<MembershipSchema, "email">): Promise<void>;

  /**
   * Updates the payment tier of an organization.
   *
   * @assumption Must be a superuser.
   *
   * @param org - The organization to update.
   * @param tier - The new payment tier.
   */
  updatePaymentTier(
    org: OrganizationSchema,
    tier: OrgPaymentTier
  ): Promise<void>;

  /**
   * As an admin, sends a password reset email, for the given account, to the admin's email.
   *
   * @assumption Must be a superuser.
   *
   * @param email - The email to reset the password of.
   */
  handleAdminPasswordReset(email: string): Promise<void>;
}
