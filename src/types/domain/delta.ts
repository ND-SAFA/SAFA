/**
 * Enumerates the types of artifact deltas.
 */
import { ArtifactSchema, TraceLinkSchema } from "@/types";

/**
 * Enumerates the types of delta state.
 */
export enum ArtifactDeltaState {
  NO_CHANGE = "NO_CHANGE",
  MODIFIED = "MODIFIED",
  ADDED = "ADDED",
  REMOVED = "REMOVED",
}

/**
 * Defines all artifact delta types.
 */
export type DeltaType = "added" | "modified" | "removed";

/**
 * Defines a modification over some delta
 */
export interface EntityModification<T> {
  before: T;
  after: T;
}

/**
 * Defines the delta entities state.
 */
export interface EntityDelta<T> {
  /**
   * A collection of all added entities.
   */
  added: Record<string, T>;
  /**
   * A collection of all removed entities.
   */
  removed: Record<string, T>;
  /**
   * A collection of all modified entities.
   */
  modified: Record<string, EntityModification<T>>;
}

/**
 * Defines the delta payload state.
 */
export interface ProjectDelta {
  /**
   * Mapping of artifact names and their corresponding changes.
   */
  artifacts: EntityDelta<ArtifactSchema>;
  /**
   * Mapping of trace ids and their corresponding changes.
   */
  traces: EntityDelta<TraceLinkSchema>;
}

/**
 * Represents an artifact delta.
 */
export type DeltaArtifact = ArtifactSchema | EntityModification<ArtifactSchema>;

/**
 * Represents a changed artifact.
 */
export interface ChangedArtifact {
  /**
   * The artifact name.
   */
  name: string;
  /**
   * The artifact delta type.
   */
  deltaType: string;
  /**
   * The changed artifact.
   */
  artifact: DeltaArtifact;
}
