import { IdentifierSchema, MembershipSchema } from "@/types";

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
   * The payment tier of this organization.
   */
  paymentTier: string;
  /**
   * List of members and their roles in the organization.
   */
  members: MembershipSchema[];
  /**
   * List of teams within the organization.
   */
  teams: TeamSchema[];
}
