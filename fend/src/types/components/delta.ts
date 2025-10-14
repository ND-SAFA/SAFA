import {
  ArtifactDeltaSchema,
  ArtifactSchema,
  EntityModificationSchema,
  TraceLinkSchema,
} from "@/types";

/**
 * Defines all artifact delta types.
 */
export type DeltaType = "added" | "modified" | "removed";

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
  artifact: ArtifactDeltaSchema;
}

/**
 * The props for displaying an artifact's diff between changes.
 */
export interface ArtifactDeltaDiffProps {
  /**
   * Whether the modal is open.
   */
  open: boolean;
  /**
   * The changed artifact to display.
   */
  delta: ChangedArtifact;
}

/**
 * The props for displaying an artifact delta button.
 */
export interface ArtifactDeltaButtonProps {
  /**
   * The changed entity name.
   */
  name: string;
  /**
   * The type of change delta for this entity.
   */
  deltaType: DeltaType;
}

/**
 * The props for displaying an artifact delta button group.
 */
export interface ArtifactDeltaButtonGroupProps {
  /**
   * The change type for this group.
   */
  deltaType: DeltaType;
  /**
   * A collection of all items with this type of change, keyed by id.
   */
  items: Record<
    string,
    ArtifactSchema | EntityModificationSchema<ArtifactSchema> | TraceLinkSchema
  >;
  /**
   *  If true, items will be interpreted as traces instead of artifacts.
   */
  isTraces?: boolean;
}
