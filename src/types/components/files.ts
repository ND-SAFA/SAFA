import { TraceLink, Artifact } from "@/types";

/**
 * Defines a project file.
 */
export interface ProjectFile {
  /**
   * The file, if loaded.
   */
  file?: File;
  /**
   * Any errors with the file.
   */
  errors: string[];
  isValid: boolean;
}

/**
 * Defines a project artifact file.
 */
export interface ArtifactFile extends ProjectFile {
  /**
   * The artifact type.
   */
  type: string;
  /**
   * A list of artifacts from the file.
   */
  artifacts: Artifact[];
}

/**
 * Defines a project trace file.
 */
export interface TraceFile extends ProjectFile {
  /**
   * The source type of the trace file.
   */
  sourceId: string;
  /**
   * The target type of the trace file.
   */
  targetId: string;
  /**
   * If true, the trace file should be generated.
   */
  isGenerated: boolean;
  /**
   * A list of traces from the file.
   */
  traces: TraceLink[];
}
