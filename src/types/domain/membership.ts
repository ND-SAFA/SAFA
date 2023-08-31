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
 * Represents a role with certain authorization constraints
 * within a given project.
 */
export enum MemberRole {
  VIEWER = "VIEWER",
  EDITOR = "EDITOR",
  ADMIN = "ADMIN",
  OWNER = "OWNER",
}

/**
 * Represents the type of entity associated with a membership.
 */
export interface MemberEntitySchema {
  /**
   * TODO: required
   * The type of entity that this member is a part of.
   */
  entityType?: MembershipType;
  /**
   * TODO: required
   * The id of the entity that this member is a part of.
   */
  entityId?: string;
}

/**
 * Represents a member in a given project
 */
export interface MembershipSchema extends MemberEntitySchema {
  /**
   * The id of this membership.
   */
  projectMembershipId: string;
  /**
   * The email of the member.
   */
  email: string;
  /**
   * The role(s) of the member.
   */
  role: MemberRole;
}

/**
 * Represents a request for adding a member to a project.
 */
export interface MemberRequestSchema {
  memberEmail: string;
  projectRole: MemberRole;
}
