import { ArtifactModel, ModelType } from "@/types";

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
}
