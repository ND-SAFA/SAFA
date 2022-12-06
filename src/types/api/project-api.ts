import {
  ArtifactSchema,
  GeneratedMatrixSchema,
  ProjectSchema,
  TraceLinkSchema,
} from "@/types/domain";

/**
 * Defines the response from checking if an artifact exists.
 */
export interface NameValidationSchema {
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
   * The project entities to commit.
   */
  project: ProjectSchema;
  /**
   * The trace generation request to perform and commit.
   */
  requests: GeneratedMatrixSchema[];
}
