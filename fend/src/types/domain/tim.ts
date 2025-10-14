/**
 * Defines a type of artifact in a project.
 */
export interface ArtifactTypeSchema {
  /**
   * The UUID for specific artifact type.
   */
  typeId: string;
  /**
   * The name of this type of artifacts.
   */
  name: string;

  /**
   * The icon that should be used to represent it.
   */
  icon: string;
  /**
   * The color of this artifact type.
   */
  color: string;

  /**
   * @readonly
   * The number of artifacts of this artifact type.
   */
  count: number;
}

/**
 * Defines a trace matrix in the project.
 */
export interface TraceMatrixSchema {
  /**
   * The UUID for this trace matrix.
   */
  id: string;
  /**
   * @readonly
   * The type of the artifact that this matrix links from.
   */
  sourceType: string;
  /**
   * @readonly
   * The type of the artifact that this matrix links to.
   */
  targetType: string;

  /**
   * @readonly
   * The total number of trace links between these types.
   */
  count: number;
  /**
   * @readonly
   * The number of trace links between these types that were generated.
   */
  generatedCount: number;
  /**
   * @readonly
   * The number of trace links between these types that were generated and approved.
   */
  approvedCount: number;
}
