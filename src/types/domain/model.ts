import { GeneratedMatrixSchema, ModelType, VersionSchema } from "@/types";

/**
 * Represents a model trained to generate trace links.
 */
export interface GenerationModelSchema {
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
  /**
   * The logged steps of training on this model.
   */
  steps?: TrainingStepSchema[];
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
export interface ArtifactLevelSchema {
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
export interface TrainOrGenerateLinksSchema {
  /**
   * The version to commit the entities to.
   */
  projectVersion?: VersionSchema;
  /**
   * The sets of matrices to generate or train on.
   */
  requests: GeneratedMatrixSchema[];
}

/**
 * Represents a step of model training.
 */
export interface TrainingStepSchema {
  /**
   * The type of training being done.
   *
   * `keywords` - Pre-Training: Keywords
   * `document` - Pre-Training: Documents
   * `repository` - Intermediate-Training: Repositories
   * `project` - Fine-Tuning: Project Data
   */
  type: "keywords" | "document" | "repository" | "project";
  /**
   * The ISO timestamp of when this step was last updated.
   */
  updatedAt: string;
  /**
   * The status of this training step.
   */
  status: "In Progress" | "Completed" | "Failed";
  /**
   * On the keywords step, any keywords to compile
   * documents and repositories using.
   */
  keywords: string[];
  /**
   * On the documents step, any documents being trained on.
   */
  documents: {
    /**
     * The name of this document.
     */
    name: string;
    /**
     * The link to where this document is stored.
     */
    url: string;
  }[];
  /**
   * On the repositories step, any GitHub repositories being trained on.
   */
  repositories: {
    /**
     * The name of this repository.
     */
    name: string;
    /**
     * The link to where this repository is stored.
     */
    url: string;
  }[];
  /**
   * On the training step, any projects being trained on.
   */
  projects: {
    /**
     * The project's id.
     */
    id: string;
    /**
     * The project's name.
     */
    name: string;
    /**
     * The trace matrices being used for training.
     */
    levels: ArtifactLevelSchema[];
  }[];
}
