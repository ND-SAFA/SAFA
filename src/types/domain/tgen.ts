import { GeneratedMatrixSchema, VersionSchema } from "@/types";

/**
 * Describes a matrix of artifacts.
 */
export interface MatrixSchema {
  /**
   * The source artifact type.
   */
  source: string;
  /**
   * The target artifact type.
   */
  target: string;
}

/**
 * Represents a matrix to generate or train links on.
 */
export interface GenerateLinksSchema {
  /**
   * The version to commit the entities to.
   */
  projectVersion?: VersionSchema;
  /**
   * The sets of matrices to generate or train on.
   */
  requests: GeneratedMatrixSchema[];
}
