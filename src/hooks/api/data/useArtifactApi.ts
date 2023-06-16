import { defineStore } from "pinia";

import { computed, ref, watch } from "vue";
import { ArtifactSchema, IOHandlerCallback } from "@/types";
import {
  useApi,
  artifactStore,
  logStore,
  projectStore,
  traceApiStore,
  traceStore,
  artifactCommitApiStore,
  artifactSaveStore,
} from "@/hooks";
import { getDoesArtifactExist } from "@/api";
import { pinia } from "@/plugins";

export const useArtifactApi = defineStore("artifactApi", () => {
  const artifactApi = useApi("artifactApi");
  const artifactNameApi = useApi("artifactNameApi");

  const nameCheckTimer = ref<ReturnType<typeof setTimeout> | undefined>();
  const nameLoading = ref(false);

  const loading = computed(() => artifactApi.loading);

  const nameError = computed(() =>
    nameLoading.value ? false : artifactSaveStore.nameError
  );

  /**
   * Verifies that the edited artifact's name is unique.
   */
  async function handleCheckName(): Promise<void> {
    await artifactNameApi.handleRequest(async () => {
      const { name } = artifactSaveStore.editedArtifact;

      if (nameCheckTimer.value) {
        clearTimeout(nameCheckTimer.value);
      }

      artifactSaveStore.isNameValid = false;
      nameLoading.value = true;

      nameCheckTimer.value = setTimeout(() => {
        if (!name) {
          artifactSaveStore.isNameValid = false;
          nameLoading.value = false;
        } else if (!artifactSaveStore.hasNameChanged) {
          artifactSaveStore.isNameValid = true;
          nameLoading.value = false;
        } else {
          getDoesArtifactExist(projectStore.versionId, name)
            .then((nameExists) => {
              artifactSaveStore.isNameValid = !nameExists;
              nameLoading.value = false;
            })
            .catch(() => {
              artifactSaveStore.isNameValid = false;
              nameLoading.value = false;
            });
        }
      }, 500);
    });
  }

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

  // Check the name is unique when the artifact name is edited.
  watch(
    () => artifactSaveStore.editedArtifact.name,
    () => handleCheckName()
  );

  // Update the artifact type when the artifact type is edited.
  watch(
    () => artifactSaveStore.editedArtifact.type,
    () => artifactSaveStore.updateArtifactType()
  );

  return {
    loading,
    nameLoading,
    nameError,
    handleSave,
    handleDuplicate,
    handleDelete,
  };
});

export default useArtifactApi(pinia);
