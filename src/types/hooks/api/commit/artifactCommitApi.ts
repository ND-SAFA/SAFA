import { ArtifactSchema, TraceLinkSchema } from "@/types";

/**
 * A hook for calling artifact commit API endpoints.
 */
export interface ArtifactCommitApiHook {
  /**
   * Creates a new artifact in the given version.
   *
   * @param versionId - The version that the artifact is stored within.
   * @param artifact - The artifact to create.
   * @return The created artifact.
   */
  handleCreate(
    versionId: string,
    artifact: ArtifactSchema
  ): Promise<ArtifactSchema[]>;
  /**
   * Updates the artifact in the given version.
   *
   * @param versionId - The version that the artifact is stored within.
   * @param artifact - The artifact to updated.
   * @return The updated artifact.
   */
  handleUpdate(
    versionId: string,
    artifact: ArtifactSchema
  ): Promise<ArtifactSchema[]>;
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
