import { ArtifactDeltaSchema } from "@/types";

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
