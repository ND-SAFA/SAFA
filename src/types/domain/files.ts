/**
 * Defines a resource file.
 */
export interface Resource {
  /**
   * The file path.
   */
  file: string;
}

/**
 * Defines a trace matrix file.
 */
export interface TraceMatrixFile extends Resource {
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
 * A collection of resources.
 */
export interface DataFile {
  [key: string]: Resource;
}

/**
 * A collection of tim files.
 */
export interface TimFile {
  [key: string]: DataFile | TraceMatrixFile;
}
