import { ArtifactLevelModel, ModelType, TrainedModel } from "@/types/domain";

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
 * Defines a trace matrix file.
 */
export interface TraceMatrixModel extends ResourceModel, ArtifactLevelModel {}

/**
 * Defines a trace matrix generation request.
 */
export interface GeneratedMatrixModel {
  /**
   * The default model to use to generate links.
   */
  method: ModelType;
  /**
   * The custom model used to generate links.
   */
  model?: TrainedModel;
  /**
   * The artifact levels to trace with method.
   */
  artifactLevels: ArtifactLevelModel[];
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
