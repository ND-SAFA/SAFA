import {
  ArtifactLevelSchema,
  ModelType,
  GenerationModelSchema,
} from "@/types/domain";

/**
 * Defines a resource file.
 */
export interface ResourceSchema {
  /**
   * The file path.
   */
  file: string;
}

/**
 * Defines a trace matrix file.
 */
export interface TraceMatrixSchema
  extends ResourceSchema,
    ArtifactLevelSchema {}

/**
 * Defines a trace matrix generation request.
 */
export interface GeneratedMatrixSchema {
  /**
   * The default model to use to generate links.
   */
  method: ModelType;
  /**
   * The custom model used to generate links.
   */
  model?: GenerationModelSchema;
  /**
   * The artifact levels to trace with method.
   */
  artifactLevels: ArtifactLevelSchema[];
}

/**
 * A collection of resources.
 */
export interface FileSchema {
  [key: string]: ResourceSchema;
}

/**
 * A collection of tim files.
 */
export interface TimFileSchema {
  [key: string]: FileSchema | TraceMatrixSchema;
}
