import { defineStore } from "pinia";

import { computed, ref, watch } from "vue";
import { ArtifactSchema, IOHandlerCallback, ArtifactApiHook } from "@/types";
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

/**
 * A hook for handling artifact API requests.
 * - Watches the `artifactSaveStore` to perform updates when the artifact `type` and `name` change.
 */
export const useArtifactApi = defineStore(
  "artifactApi",
  (): ArtifactApiHook => {
    const artifactSaveApi = useApi("artifactSaveApi");
    const artifactDeleteApi = useApi("artifactDeleteApi");
    const artifactNameApi = useApi("artifactNameApi");

    const nameCheckTimer = ref<ReturnType<typeof setTimeout> | undefined>();
    const nameLoading = ref(false);

    const saveLoading = computed(() => artifactSaveApi.loading);
    const deleteLoading = computed(() => artifactDeleteApi.loading);

    const nameError = computed(() =>
      nameLoading.value ? false : artifactSaveStore.nameError
    );

    async function handleCheckName(): Promise<void> {
      await artifactNameApi.handleRequest(async () => {
        const name = artifactSaveStore.editedArtifact.name || "";

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

    async function handleSave(
      artifact: ArtifactSchema,
      isUpdate: boolean,
      parentArtifact: ArtifactSchema | undefined,
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await artifactSaveApi.handleRequest(
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
                await traceApiStore.handleCreate(
                  createdArtifact,
                  parentArtifact
                );
              }
            }
          }
        },
        {
          ...callbacks,
          success: isUpdate
            ? `Edited artifact: ${artifact.name}`
            : `Created a new artifact: ${artifact.name}`,
          error: `Unable to save artifact: ${artifact.name}`,
        }
      );
    }

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

          await artifactDeleteApi.handleRequest(
            async () => {
              await artifactCommitApiStore.handleDelete(
                artifact,
                relatedTraces
              );

              artifactStore.deleteArtifacts([artifact]);
              traceStore.deleteTraceLinks(relatedTraces);
            },
            {
              ...callbacks,
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
      saveLoading,
      deleteLoading,
      nameLoading,
      nameError,
      handleSave,
      handleDelete,
      handleCheckName,
    };
  }
);

export default useArtifactApi(pinia);
