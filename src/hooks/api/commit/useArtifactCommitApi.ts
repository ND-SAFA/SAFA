import { defineStore } from "pinia";

import { ApprovalType, ArtifactSchema, TraceLinkSchema } from "@/types";
import { commitApiStore } from "@/hooks";
import { pinia } from "@/plugins";

export const useArtifactCommitApi = defineStore("artifactCommitApi", () => {
  /**
   * Creates a new artifact in the given version.
   *
   * @param versionId - The version that the artifact is stored within.
   * @param artifact - The artifact to create.
   * @return The created artifact.
   */
  async function handleCreate(
    versionId: string,
    artifact: ArtifactSchema
  ): Promise<ArtifactSchema[]> {
    return commitApiStore
      .handleSave((builder) => builder.withNewArtifact(artifact))
      .then((commit) => commit?.artifacts.added || []);
  }

  /**
   * Updates the artifact in the given version.
   *
   * @param versionId - The version that the artifact is stored within.
   * @param artifact - The artifact to updated.
   * @return The updated artifact.
   */
  async function handleUpdate(
    versionId: string,
    artifact: ArtifactSchema
  ): Promise<ArtifactSchema[]> {
    return commitApiStore
      .handleSave((builder) => builder.withModifiedArtifact(artifact))
      .then((commit) => commit?.artifacts.modified || []);
  }

  /**
   * Deletes artifact in project version specified.
   *
   * @param artifact - The artifact to delete.
   * @param traceLinks - Any related trace links to also delete.
   * @return The deleted artifact.
   */
  async function handleDelete(
    artifact: ArtifactSchema,
    traceLinks: TraceLinkSchema[]
  ): Promise<ArtifactSchema> {
    traceLinks = traceLinks.map((link) => ({
      ...link,
      approvalStatus: ApprovalType.DECLINED,
    }));

    return commitApiStore
      .handleSave((builder) =>
        builder
          .withRemovedArtifact(artifact)
          .withModifiedTraceLink(...traceLinks)
      )
      .then(() => artifact);
  }

  return { handleCreate, handleUpdate, handleDelete };
});

export default useArtifactCommitApi(pinia);
