import { Artifact } from "@/types";

/**
 * Represents an item in an artifact search list.
 */
export type ArtifactSearchItem =
  | Artifact
  | { header: string }
  | { divider: boolean };
