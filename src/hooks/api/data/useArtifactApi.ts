import { defineStore } from "pinia";

import { computed } from "vue";
import { ArtifactSchema, IOHandlerCallback } from "@/types";
import {
  useApi,
  artifactStore,
  logStore,
  projectStore,
  traceApiStore,
  traceStore,
  artifactCommitApiStore,
} from "@/hooks";
import { pinia } from "@/plugins";

export const useArtifactApi = defineStore("artifactApi", () => {
  const artifactApi = useApi("artifactApi");

  const loading = computed(() => artifactApi.loading);

  /**
   * Creates or updates an artifact, and updates app state.
   *
   * @param artifact - The artifact to create.
   * @param isUpdate - Whether this operation should label this commit as
   * updating a previously existing artifact.
   * @param parentArtifact - The parent artifact to link to.
   * @param callbacks - Callbacks to run after the action.
   */
  async function handleSave(
    artifact: ArtifactSchema,
    isUpdate: boolean,
    parentArtifact: ArtifactSchema | undefined,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await artifactApi.handleRequest(
      async () => {
        const versionId = projectStore.versionIdWithLog;

        if (isUpdate) {
          const updatedArtifacts = await artifactCommitApiStore.handleUpdate(
            versionId,
            artifact
          );

          artifactStore.addOrUpdateArtifacts(updatedArtifacts);
        } else {
          const createdArtifacts = await artifactCommitApiStore.handleCreate(
            versionId,
            artifact
          );

          artifactStore.addCreatedArtifact(createdArtifacts[0]);

          if (parentArtifact) {
            for (const createdArtifact of createdArtifacts) {
              await traceApiStore.handleCreate(createdArtifact, parentArtifact);
            }
          }
        }
      },
      callbacks,
      {
        success: isUpdate
          ? `Edited artifact: ${artifact.name}`
          : `Created a new artifact: ${artifact.name}`,
        error: `Unable to save artifact: ${artifact.name}`,
      }
    );
  }

  /**
   * Duplicates an artifact, and updates the app state.
   *
   * @param artifact  - The artifact to duplicate.
   * @param callbacks - Callbacks to run after the action.
   */
  function handleDuplicate(
    artifact: ArtifactSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    return handleSave(
      {
        ...artifact,
        name: artifact.name + " (Copy)",
        id: "",
        baseEntityId: "",
      },
      false,
      undefined,
      callbacks
    );
  }

  /**
   * Deletes an artifact, and updates the app state.
   *
   * @param artifact  - The artifact to delete.
   * @param callbacks - Callbacks to run after the action.
   */
  function handleDelete(
    artifact: ArtifactSchema,
    callbacks: IOHandlerCallback = {}
  ): void {
    logStore.confirm(
      "Delete Artifact",
      `Are you sure you would like to delete "${artifact.name}"?`,
      async (isConfirmed: boolean) => {
        if (!isConfirmed) return;

        const relatedTraces = traceStore.allTraces.filter(
          ({ sourceId, targetId }) =>
            sourceId === artifact.id || targetId === artifact.id
        );

        await artifactApi.handleRequest(
          async () => {
            await artifactCommitApiStore.handleDelete(artifact, relatedTraces);

            artifactStore.deleteArtifacts([artifact]);
            traceStore.deleteTraceLinks(relatedTraces);
          },
          callbacks,
          {
            success: `Deleted artifact: ${artifact.name}`,
            error: `Unable to delete artifact: ${artifact.name}`,
          }
        );
      }
    );
  }

  return { loading, handleSave, handleDuplicate, handleDelete };
});

export default useArtifactApi(pinia);
