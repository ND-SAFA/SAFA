/**
 * Defines a resource file.
 */
export interface ResourceModel {
  /**
   * The file path.
   */
  file: string;
}

/**
 * Defines a type matrix.
 */
export interface TypeMatrixModel {
  /**
   * The source type to trace from.
   */
  source: string;
  /**
   * The target type to trace to.
   */
  target: string;
}

/**
 * Defines a trace matrix file.
 */
export interface TraceMatrixModel extends ResourceModel, TypeMatrixModel {}

/**
 * A collection of resources.
 */
export interface FileModel {
  [key: string]: ResourceModel;
}

/**
 * A collection of tim files.
 */
export interface TimFileModel {
  [key: string]: FileModel | TraceMatrixModel;
}
