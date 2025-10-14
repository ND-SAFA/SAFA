import { defineStore } from "pinia";

import { computed, ref, watch } from "vue";
import { ArtifactApiHook, ArtifactSchema, IOHandlerCallback } from "@/types";
import { ENABLED_FEATURES } from "@/util";
import {
  appStore,
  artifactCommitApiStore,
  artifactSaveStore,
  artifactStore,
  documentStore,
  logStore,
  selectionStore,
  traceApiStore,
  traceStore,
  useApi,
} from "@/hooks";
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
          } else if (!ENABLED_FEATURES.ARTIFACT_NAME_CHECK) {
            artifactSaveStore.isNameValid = true;
            nameLoading.value = false;
          } else {
            artifactSaveStore.isNameValid = false;
            nameLoading.value = false;
          }
        }, 500);
      });
    }

    async function handleSave(
      artifact: ArtifactSchema,
      isUpdate: boolean,
      parentArtifacts: ArtifactSchema[] = [],
      childArtifacts: ArtifactSchema[] = [],
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await artifactSaveApi.handleRequest(
        async () => {
          if (isUpdate) {
            const updatedArtifacts =
              await artifactCommitApiStore.handleUpdate(artifact);

            artifactStore.addOrUpdateArtifacts(updatedArtifacts);
          } else {
            const createdArtifacts =
              await artifactCommitApiStore.handleCreate(artifact);

            documentStore.addDocumentArtifacts([createdArtifacts[0].id]);
            artifactStore.addCreatedArtifact(createdArtifacts[0]);
            selectionStore.selectArtifact(createdArtifacts[0].id);

            for (const createdArtifact of createdArtifacts) {
              for (const parentArtifact of parentArtifacts) {
                await traceApiStore.handleCreate(
                  createdArtifact,
                  parentArtifact
                );
              }
              for (const childArtifact of childArtifacts) {
                await traceApiStore.handleCreate(
                  childArtifact,
                  createdArtifact
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
              selectionStore.clearSelections();
              appStore.closeSidePanels();
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
