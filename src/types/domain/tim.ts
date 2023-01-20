/**
 * Defines an artifact level in the project.
 */
export interface TimArtifactLevelSchema {
  /**
   * The type of the artifact.
   */
  artifactType: string;
  /**
   * The number of artifacts of this artifact type.
   */
  count: number;
}

/**
 * Defines a trace matrix in the project.
 */
export interface TimTraceMatrixSchema {
  /**
   * The type of the artifact that this matrix links from.
   */
  sourceType: string;
  /**
   * The type of the artifact that this matrix links to.
   */
  targetType: string;
  /**
   * The number of artifacts of this artifact type.
   */
  count: number;
}

/**
 * Defines the structure of a TIM project graph.
 */
export interface TimSchema {
  /**
   * The artifact levels in the project.
   */
  artifacts: TimArtifactLevelSchema[];
  /**
   * The trace matrices in the project
   */
  traces: TimTraceMatrixSchema[];
}
