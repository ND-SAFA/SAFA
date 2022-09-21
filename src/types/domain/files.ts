/**
 * Defines a resource file.
 */
import { ModelType, TrainedModel } from "@/types";

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
 * Defines a trace matrix generation request.
 */
export interface GeneratedMatrixModel extends TypeMatrixModel {
  /**
   * The default model to use to generate links.
   */
  method: ModelType;
  /**
   * The custom model used to generate links.
   */
  model?: TrainedModel;
}

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
