import { ArtifactSchema, TraceLinkSchema } from "@/types";

/**
 * A hook for calling artifact commit API endpoints.
 */
export interface ArtifactCommitApiHook {
  /**
   * Creates a new artifact in the given version.
   *
   * @param artifacts - The artifacts to create.
   * @return The created artifact.
   */
  handleCreate(...artifacts: ArtifactSchema[]): Promise<ArtifactSchema[]>;
  /**
   * Updates the artifact in the given version.
   *
   * @param artifacts - The artifacts to update.
   * @return The updated artifact.
   */
  handleUpdate(...artifacts: ArtifactSchema[]): Promise<ArtifactSchema[]>;
  /**
   * Deletes artifact in project version specified.
   *
   * @param artifact - The artifact to delete.
   * @param traceLinks - Any related trace links to also delete.
   * @return The deleted artifact.
   */
  handleDelete(
    artifact: ArtifactSchema,
    traceLinks: TraceLinkSchema[]
  ): Promise<ArtifactSchema>;
}
