/**
 * The types of permissions allowed on an organization.
 */
export type OrganizationPermissionType = "navigation" | "viewer" | "editor";

/**
 * The types of permissions allowed on a project.
 */
export type ProjectPermissionType = "viewer" | "editor" | "admin" | "owner";

/**
 * Represents a member in a given project
 */
export interface MembershipSchema {
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
  role: ProjectRole;
  /**
   * TODO: required
   * The type of entity that this member is a part of.
   */
  variant?: MembershipType;
  /**
   * TODO: required
   * The id of the entity that this member is a part of.
   */
  entityId?: string;
}

/**
 * Represents a role with certain authorization constraints
 * within a given project.
 */
export enum ProjectRole {
  VIEWER = "VIEWER",
  EDITOR = "EDITOR",
  ADMIN = "ADMIN",
  OWNER = "OWNER",
}

/**
 * The types of entities that a user can be a member of.
 */
export type MembershipType = "ORGANIZATION" | "TEAM" | "PROJECT";

/**
 * Represents a request for adding a member to a project.
 */
export interface MemberRequestSchema {
  memberEmail: string;
  projectRole: ProjectRole;
}
