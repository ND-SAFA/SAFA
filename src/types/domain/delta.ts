/**
 * Enumerates the types of artifact deltas.
 */
export enum ArtifactDeltaState {
  NO_CHANGE = "no_change",
  MODIFIED = "modified",
  ADDED = "added",
  REMOVED = "removed",
}

/**
 * Defines an added artifact delta.
 */
export interface AddedArtifact {
  after: string;
}

/**
 * Defines a removed artifact delta.
 */
export interface RemovedArtifact {
  before: string;
}

/**
 * Defines a modified artifact delta.
 */
export interface ModifiedArtifact {
  before: string;
  after: string;
}

/**
 * Defines all types of artifact deltas.
 */
export type DeltaArtifact = AddedArtifact | RemovedArtifact | ModifiedArtifact;

/**
 * Defines all artifact delta types.
 */
export type DeltaType = "added" | "modified" | "removed";
