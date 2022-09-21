import {
  ArtifactModel,
  ModelType,
  TraceLinkModel,
  TrainedModel,
  VersionModel,
} from "@/types";

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

/**
 * Represents a matrix to train on links between.
 */
export interface TrainOnLinksModel {
  /**
   * THe project that this model belongs to.
   */
  projectId: string;
  /**
   * The source artifacts.
   */
  sources: ArtifactModel[];
  /**
   * The target artifacts.
   */
  targets: ArtifactModel[];
  /**
   * The trace links to train on.
   */
  traces: TraceLinkModel[];
  /**
   * The custom trained model to use for generation.
   */
  model: TrainedModel;
}
