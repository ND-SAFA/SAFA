import {
  ArtifactLevelSchema,
  ModelType,
  GenerationModelSchema,
} from "@/types/domain";

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
