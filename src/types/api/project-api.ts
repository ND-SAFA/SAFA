import {
  ArtifactSchema,
  GeneratedMatrixSchema,
  ProjectSchema,
  TraceLinkSchema,
} from "@/types/domain";

/**
 * Defines the request for checking if an artifact exists.
 */
export interface NameValidationRequestSchema {
  /**
   * The artifact name to check.
   */
  artifactName: string;
}

/**
 * Defines the response from checking if an artifact exists.
 */
export interface NameValidationResponseSchema {
  /**
   * Whether the artifact exists.
   */
  artifactExists: boolean;
}

/**
 * The response from parsing a file.
 */
export interface ParseFileSchema {
  /**
   * Any parsing errors encountered.
   */
  errors: string[];
}

/**
 * The response from parsing an artifact file.
 */
export interface ParseArtifactFileSchema extends ParseFileSchema {
  /**
   * The artifacts parsed.
   */
  entities: ArtifactSchema[];
}

/**
 * The response from parsing a trace file.
 */
export interface ParseTraceFileSchema extends ParseFileSchema {
  /**
   * The traces parsed.
   */
  entities: TraceLinkSchema[];
}

/**
 * The request payload for creating a project via JSON.
 */
export interface CreateProjectByJsonSchema {
  /**
   * The organization to create the project for.
   */
  orgId: string;
  /**
   * The team to create the project for.
   */
  teamId: string;
  /**
   * The project entities to commit.
   */
  project: ProjectSchema;
  /**
   * The trace generation request to perform and commit.
   */
  requests: GeneratedMatrixSchema[];
}

/**
 * The types of project owners.
 */
export type ProjectOwnerType =
  | "ORGANIZATION"
  | "TEAM"
  | "USER_ID"
  | "USER_EMAIL";

/**
 * Represents a request to transfer ownership of a project.
 */
export interface TransferProjectSchema {
  /**
   * The new owner of the project, which will be either a UUID
   * or an email specifically in the case of ownerType == USER_EMAIL
   */
  owner: string;
  /**
   * The type of owner, to transfer to.
   */
  ownerType: ProjectOwnerType;
}
