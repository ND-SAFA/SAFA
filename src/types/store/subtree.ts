/**
 * Request used to identify which nodes and edges to target
 * for the opacity change.
 */
export interface SetOpacityRequest {
  targetArtifactIds: string[];
  visible: boolean;
}
