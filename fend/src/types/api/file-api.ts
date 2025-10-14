/**
 Represents the project TIM file artifact format.
 */
export interface TimArtifactJsonSchema {
  /**
   * The name of the artifact type for these artifacts.
   */
  type: string;
  /**
   * The name of the file containing artifacts.
   */
  fileName: string;
}

/**
 Represents the project TIM file trace link format.
 */
export interface TimTraceJsonSchema {
  /**
   * The name of the artifact source type for these trace links.
   */
  sourceType: string;
  /**
   * The name of the artifact target type for these trace links.
   */
  targetType: string;
  /**
   * The name of the file containing trace links.
   * Must be included unless `generateLinks` is set to true.
   */
  fileName?: string;
  /**
   * The name of the file containing trace links.
   */
  generateLinks?: boolean;
}

/**
 Represents the project TIM file format.
 */
export interface TimJsonSchema {
  /**
   * A collection of descriptors for each artifact file.
   */
  artifacts: TimArtifactJsonSchema[];
  /**
   * A collection of descriptors for each trace file.
   */
  traces: TimTraceJsonSchema[];
}
