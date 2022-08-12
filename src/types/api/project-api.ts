import { Artifact, TraceLink } from "@/types/domain";

/**
 * Defines the response from checking if an artifact exists.
 */
export interface NameValidationModel {
  /**
   * Whether the artifact exists.
   */
  artifactExists: boolean;
}

/**
 * The response from parsing a file.
 */
export interface ParseFileModel {
  /**
   * Any parsing errors encountered.
   */
  errors: string[];
}

/**
 * The response from parsing an artifact file.
 */
export interface ParseArtifactFileModel extends ParseFileModel {
  /**
   * The artifacts parsed.
   */
  entities: Artifact[];
}

/**
 * The response from parsing a trace file.
 */
export interface ParseTraceFileModel extends ParseFileModel {
  /**
   * The traces parsed.
   */
  entities: TraceLink[];
}

/**
 * Represents a member in a given project
 */
export interface MembershipModel {
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
export interface MemberRequestModel {
  memberEmail: string;
  projectRole: ProjectRole;
}
