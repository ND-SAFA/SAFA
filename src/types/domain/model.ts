import { GeneratedMatrixModel, ModelType, VersionModel } from "@/types";

/**
 * Represents a model trained to generate trace links.
 */
export interface GenerationModel {
  /**
   * The model's id.
   */
  id: string;
  /**
   * The model's name.
   */
  name: string;
  /**
   * The base model that is being extended.
   */
  baseModel: ModelType;
}

/**
 * Lists the methods by which a model can be shared.
 */
export enum ModelShareType {
  CLONE = "COPY_BY_VALUE",
  REUSE = "COPY_BY_REFERENCE",
}

/**
 * Describes a matrix of artifacts.
 */
export interface ArtifactLevelModel {
  /**
   * The source artifact type.
   */
  source: string;
  /**
   * The target artifact type.
   */
  target: string;
}

/**
 * Represents a matrix to generate or train links on.
 */
export interface TrainOrGenerateLinksModel {
  /**
   * The version to commit the entities to.
   */
  projectVersion?: VersionModel;
  /**
   * The sets of matrices to generate or train on.
   */
  requests: GeneratedMatrixModel[];
}
