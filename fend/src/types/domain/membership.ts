/**
 * The types of permissions allowed on an organization.
 */
export type OrganizationPermissionType = "navigation" | "viewer" | "editor";

/**
 * The types of permissions allowed on a project.
 */
export type ProjectPermissionType = "viewer" | "editor" | "admin" | "owner";

/**
 * The types of entities that a user can be a member of.
 */
export type MembershipType = "ORGANIZATION" | "TEAM" | "PROJECT";

/**
 * The types of permissions allowed on an organization, team, or project.
 */
export type MemberRole =
  | "PENDING" // a temporary role for a user who has been invited but not yet accepted
  | "NONE" // project, team, org
  | "VIEWER" // project, team
  | "EDITOR" // project, team
  | "GENERATOR" // project, team, org
  | "ADMIN" // project, team, org
  | "OWNER" // project
  | "MEMBER" // org
  | "BILLING_MANAGER"; // org

/**
 * The types of permissions allowed on an organization, team, or project.
 */
export type PermissionType =
  | "safa.view"
  | "safa.view_admin"
  | "safa.create_orgs"
  | "org.delete_teams"
  | "org.create_teams"
  | "org.view_teams"
  | "org.delete"
  | "org.edit"
  | "org.view_billing"
  | "org.view"
  | "org.edit_members"
  | "team.delete_projects"
  | "team.create_projects"
  | "team.view_projects"
  | "team.delete"
  | "team.edit_members"
  | "team.edit"
  | "team.view"
  | "project.delete"
  | "project.generate"
  | "project.edit"
  | "project.edit_members"
  | "project.edit_data"
  | "project.edit_versions"
  | "project.edit_integrations"
  | "project.view";

/**
 * Represents the type of entity associated with a membership.
 */
export interface MemberEntitySchema {
  /**
   * The type of entity that this member is a part of.
   */
  entityType: MembershipType;
  /**
   * The id of the entity that this member is a part of.
   */
  entityId: string;
}

/**
 * Represents a request to create a shareable project link with other members.
 */
export interface InviteMembershipSchema {
  /**
   * The email of the member.
   * If empty, no invite email will be sent.
   */
  email?: string;
  /**
   * The role(s) of the member.
   */
  role: MemberRole;
}

/**
 * Represents a request to create a shareable project link with other members.
 */
export interface InviteTokenSchema {
  /**
   * The token which can be passed to the accept endpoint.
   */
  token: string;

  /**
   * The time at which the token will expire.
   */
  expiration: string;

  /**
   * The URL the user can use to accept the invitation.
   * This is currently set to https://<front-end>/accept-invite?token=<token>
   */
  url: string;
}

/**
 * Represents a member in a given project
 */
export interface MembershipSchema
  extends MemberEntitySchema,
    Required<InviteMembershipSchema> {
  /**
   * The id of this membership.
   */
  id: string;
  /**
   * Whether the user is currently logged in.
   */
  active?: boolean;
}
