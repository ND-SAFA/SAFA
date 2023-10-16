import { IdentifierSchema, MembershipSchema, PermissionType } from "@/types";

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
  /**
   * The permissions of the current user on this organization.
   */
  permissions: PermissionType[];
}
