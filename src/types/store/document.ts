import { Artifact, TraceLink } from "@/types";

/**
 * Defines the artifacts displayed in a document.
 */
export interface DocumentArtifacts {
  /**
   * All artifacts in the project.
   */
  artifacts: Artifact[];
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
   */
  traces: TraceLink[];
  /**
   * The artifacts that are visible in the current document.
   * If empty, all trace links are made visible.
   */
  currentArtifactIds?: string[];
}
