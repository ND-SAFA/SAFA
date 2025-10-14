import { IdentifierSchema, MembershipSchema, PermissionType } from "@/types";

/**
 * The types of payment tiers for an organization.
 */
export type OrgPaymentTier =
  | "UNLIMITED" // Can generate unlimited data
  | "RECURRING" // Can generate unlimited data, charged monthly
  | "AS_NEEDED"; // Charged per data generation

/**
 * Represents the billing information for an organization.
 */
export interface OrganizationBillingSchema {
  /**
   * The payment tier of this organization.
   */
  paymentTier: OrgPaymentTier;
  /**
   * The remaining credits for the current month.
   * For pay-as-you-go organizations, this will roll over to the next month.
   */
  monthlyRemainingCredits: number;
  /**
   * The total credits for the current month.
   */
  monthlyUsedCredits: number;
  /**
   * The total successfully used credits for the current month.
   */
  monthlySuccessfulCredits: number;
  /**
   * The total used credits for the organization.
   */
  totalUsedCredits: number;
  /**
   * The total successfully used credits for the organization.
   */
  totalSuccessfulCredits: number;
}

/**
 * Represents a team with members and projects.
 */
export interface TeamSchema {
  /**
   * The id of this team.
   */
  id: string;
  /**
   * The name of this team.
   */
  name: string;
  /**
   * List of members and their roles in the team.
   */
  members: MembershipSchema[];
  /**
   * List of projects this team has access to.
   */
  projects: IdentifierSchema[];
  /**
   * The permissions of the current user on this team.
   */
  permissions: PermissionType[];
}

/**
 * Represents an organization with members and teams.
 */
export interface OrganizationSchema {
  /**
   * The id of this organization.
   */
  id: string;
  /**
   * The name of this organization.
   */
  name: string;
  /**
   * The description of this organization.
   */
  description: string;
  /**
   * Whether this organization is for an individual user.
   */
  personalOrg: boolean;
  /**
   * List of members and their roles in the organization.
   */
  members: MembershipSchema[];
  /**
   * List of teams within the organization.
   */
  teams: TeamSchema[];
  /**
   * The permissions of the current user on this organization.
   */
  permissions: PermissionType[];
  /**
   * The billing information for this organization.
   */
  billing: OrganizationBillingSchema;
}

/**
 * The schema for updating the payment tier of an organization.
 */
export interface UpdatePaymentTierSchema {
  /**
   * The id of the organization to update.
   */
  organizationId: string;
  /**
   * The new payment tier.
   */
  tier: OrgPaymentTier;
}
