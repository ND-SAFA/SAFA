import { ArtifactModel } from "@/types";

/**
 * Represents an item in an artifact search list.
 */
export type ArtifactSearchItem =
  | ArtifactModel
  | { header: string }
  | { divider: boolean };
