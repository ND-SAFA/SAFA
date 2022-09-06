import { ArtifactModel, TraceLinkModel } from "@/types/domain";

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
  entities: ArtifactModel[];
}

/**
 * The response from parsing a trace file.
 */
export interface ParseTraceFileModel extends ParseFileModel {
  /**
   * The traces parsed.
   */
  entities: TraceLinkModel[];
}
