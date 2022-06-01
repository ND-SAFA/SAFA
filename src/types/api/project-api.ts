import {
  Artifact,
  ArtifactDeltaState,
  TraceLink,
  Project,
  ProjectVersion,
} from "@/types/domain";

/**
 * Defines the response for a created project.
 */
export interface ProjectEntities {
  /**
   * The created project.
   */
  project: Project;
}

/**
 * Defines the response from checking if an artifact exists.
 */
export interface ArtifactNameValidationResponse {
  /**
   * Whether the artifact exists.
   */
  artifactExists: boolean;
}
/**
 * Defines a changed artifact.
 */
export interface ArtifactChange {
  /**
   * The type of change to this artifact.
   */
  revisionType:
    | ArtifactDeltaState.ADDED
    | ArtifactDeltaState.MODIFIED
    | ArtifactDeltaState.REMOVED;
  /**
   * The artifact changed.
   */
  artifact: Artifact;
}

/**
 * Defines a changed trance.
 */
export interface TraceChange {
  /**
   * The type of change to this trace.
   */
  revisionType: ArtifactDeltaState.ADDED | ArtifactDeltaState.REMOVED;
  /**
   * The trace changed.
   */
  trace: TraceLink;
}

/**
 * The response from parsing a file.
 */
export interface ParseFileResponse {
  /**
   * Any parsing errors encountered.
   */
  errors: string[];
}

/**
 * The response from parsing an artifact file.
 */
export interface ParseArtifactFileResponse extends ParseFileResponse {
  /**
   * The artifacts parsed.
   */
  artifacts: Artifact[];
}

/**
 * The response from parsing a trace file.
 */
export interface ParseTraceFileResponse extends ParseFileResponse {
  /**
   * The traces parsed.
   */
  traces: TraceLink[];
}

/**
 * Represents a single commit containing one or more changes to
 * either artifacts or trace links
 */
export interface Commit {
  /**
   * The version this commit is being made on.
   */
  commitVersion: ProjectVersion;
  /**
   * The changes occurring to the project artifacts.
   */
  artifacts: EntityCommit<Artifact>;
  /**
   * The changes occurring to project traces.
   */
  traces: EntityCommit<TraceLink>;
}

/**
 * Encapsulates the changes for a generic type of project entity.
 */
export interface EntityCommit<T> {
  /**
   * The entities that were added.
   */
  added: T[];
  /**
   * The entities that were removed
   */
  removed: T[];
  /**
   * The entities that were modified.
   */
  modified: T[];
}

/**
 * Represents a member in a given project
 */
export interface ProjectMembership {
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
export interface MemberRequest {
  memberEmail: string;
  projectRole: ProjectRole;
}
