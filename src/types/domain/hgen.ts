/**
 * The schema for a request to generate parent artifacts for a set of child artifacts.
 */
export interface GenerateArtifactSchema {
  /**
   * The model to generate the artifact with.
   */
  model?: string;
  /**
   * The artifact IDs to generate a parent artifact for.
   */
  artifacts: string[];
  /**
   * The type of parent artifact to generate.
   */
  targetTypes: string[];
  /**
   * The clusters of artifact ids to generate a parent artifact for.
   * If empty, artifacts will automatically be clustered.
   * If not empty, artifacts will be clustered according to the provided clusters.
   */
  clusters?: string[][];
}
