/**
 * Enumerates the types of artifact deltas.
 */
import {
  ArtifactSchema,
  LayoutPositionsSchema,
  SubtreeMapSchema,
  TraceLinkSchema,
} from "@/types";

/**
 * Enumerates the types of delta state.
 */
export type ArtifactDeltaState =
  | "NO_CHANGE"
  | "MODIFIED"
  | "ADDED"
  | "REMOVED"
  | "IMPACTED";

/**
 * Defines a modification over some delta
 */
export interface EntityModificationSchema<Entity> {
  before: Entity;
  after: Entity;
}

/**
 * Defines the delta entities state.
 */
export interface EntityDeltaSchema<Entity> {
  /**
   * A collection of all added entities.
   */
  added: Record<string, Entity>;
  /**
   * A collection of all removed entities.
   */
  removed: Record<string, Entity>;
  /**
   * A collection of all modified entities.
   */
  modified: Record<string, EntityModificationSchema<Entity>>;
  /**
   * A collection of all impacted entities.
   */
  impacted?: Record<string, Entity>;
}

/**
 * Defines the changed project data between two versions.
 */
export interface VersionDeltaSchema {
  /**
   * Mapping of artifact names and their corresponding changes.
   */
  artifacts: EntityDeltaSchema<ArtifactSchema>;
  /**
   * Mapping of trace ids and their corresponding changes.
   */
  traces: EntityDeltaSchema<TraceLinkSchema>;
  /**
   * Map of artifact ids to their position in the delta graph.
   */
  layout?: LayoutPositionsSchema;
  /**
   * Map of delta artifact ids to their subtree information.
   */
  subtrees?: SubtreeMapSchema;
}

/**
 * Represents an artifact delta.
 */
export type ArtifactDeltaSchema =
  | ArtifactSchema
  | EntityModificationSchema<ArtifactSchema>;
