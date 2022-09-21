import { ArtifactModel, ModelType, TrainedModel, VersionModel } from "@/types";

/**
 * Represents a matrix to generate links between.
 */
export interface GenerateLinksModel {
  /**
   * The source artifacts.
   */
  sourceArtifacts: ArtifactModel[];
  /**
   * The target artifacts.
   */
  targetArtifacts: ArtifactModel[];
  /**
   * The generation method.
   */
  method: ModelType;
  /**
   * The custom trained model to use for generation.
   */
  model?: TrainedModel;
  /**
   * The version to commit the entities to.
   */
  projectVersion?: VersionModel;
}
