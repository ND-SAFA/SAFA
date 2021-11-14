/**
 * Enumerates the types of artifact deltas.
 */
import { Artifact } from "@/types";

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
export type ArtifactDelta = AddedArtifact | RemovedArtifact | ModifiedArtifact;

/**
 * Defines all artifact delta types.
 */
export type DeltaType = "added" | "modified" | "removed";

/**
 * Defines the delta artifacts state.
 */
export interface DeltaArtifacts {
  /**
   * A collection of all added artifacts.
   */
  added: Record<string, AddedArtifact>;
  /**
   * A collection of all removed artifacts.
   */
  removed: Record<string, RemovedArtifact>;
  /**
   * A collection of all modified artifacts.
   */
  modified: Record<string, ModifiedArtifact>;
}

/**
 * Defines the delta payload state.
 */
export interface DeltaPayload extends DeltaArtifacts {
  /**
   * A list of all missing artifacts.
   */
  missingArtifacts: Artifact[];
}
