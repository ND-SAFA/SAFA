/**
 * Represents a member in a given project
 */
export interface MembershipSchema {
  projectMembershipId: string;
  email: string;
  role: ProjectRole;
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
 * Represents a request for adding a member to a project.
 */
export interface MemberRequestSchema {
  memberEmail: string;
  projectRole: ProjectRole;
}
