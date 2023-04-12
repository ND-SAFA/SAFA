import { ArtifactSchema, TraceLinkSchema } from "@/types";

/**
 * Defines the artifacts displayed in a document.
 */
export interface DocumentArtifacts {
  /**
   * All artifacts in the project.
   * If empty, the current artifacts will be preserved.
   */
  artifacts?: ArtifactSchema[];
  /**
   * The artifacts that are visible in the current document.
   * If empty, all artifacts are made visible.
   */
  currentArtifactIds?: string[];
}

/**
 * Defines the trace links displayed in a document.
 */
export interface DocumentTraces {
  /**
   * All trace links in the project.
   * If empty, the current traces will be preserved.
   */
  traces?: TraceLinkSchema[];
  /**
   * The artifacts that are visible in the current document.
   * If empty, all trace links are made visible.
   */
  currentArtifactIds?: string[];
}
