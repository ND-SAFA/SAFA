import { ArtifactModel, ConfirmationType, IOHandlerCallback } from "@/types";
import {
  artifactStore,
  layoutStore,
  logStore,
  projectStore,
  selectionStore,
} from "@/hooks";
import {
  createArtifact,
  deleteArtifact,
  updateArtifact,
  handleCreateLink,
} from "@/api";

/**
 * Creates or updates an artifact, and updates app state.
 *
 * @param artifact - The artifact to create.
 * @param isUpdate - Whether this operation should label this commit as
 * updating a previously existing artifact.
 * @param parentArtifact - The parent artifact to link to.
 * @param onSuccess - Called if the save is successful.
 * @param onError - Called if the save fails.
 */
export async function handleSaveArtifact(
  artifact: ArtifactModel,
  isUpdate: boolean,
  parentArtifact: ArtifactModel | undefined,
  { onSuccess, onError }: IOHandlerCallback
): Promise<void> {
  try {
    const versionId = projectStore.versionIdWithLog;

    if (isUpdate) {
      const updatedArtifacts = await updateArtifact(versionId, artifact);

      artifactStore.addOrUpdateArtifacts(updatedArtifacts);
    } else {
      const createdArtifacts = await createArtifact(versionId, artifact);

      artifactStore.addOrUpdateArtifacts(createdArtifacts);
      selectionStore.selectArtifact(createdArtifacts[0].id);
      layoutStore.setArtifactTreeLayout();

      if (!parentArtifact) {
        onSuccess?.();
        return;
      }

      for (const createdArtifact of createdArtifacts) {
        await handleCreateLink(createdArtifact, parentArtifact);
      }
    }

    onSuccess?.();
  } catch (e) {
    logStore.onDevError(String(e));
    logStore.onError(`Unable to create artifact: ${artifact.name}`);
    onError?.(e as Error);
  }
}

/**
 * Duplicates an artifact, and updates the app state.
 *
 * @param artifact  - The artifact to duplicate.
 * @param onSuccess - Called if the duplicate is successful.
 * @param onError - Called if the duplicate fails.
 */
export function handleDuplicateArtifact(
  artifact: ArtifactModel,
  { onSuccess, onError }: IOHandlerCallback
): Promise<void> {
  return handleSaveArtifact(
    {
      ...artifact,
      name: artifact.name + " (Copy)",
      id: "",
      baseEntityId: "",
    },
    false,
    undefined,
    { onSuccess, onError }
  );
}

/**
 * Deletes an artifact, and updates the app state.
 *
 * @param artifact  - The artifact to delete.
 * @param onSuccess - Called if the delete is successful.
 * @param onError - Called if the delete fails.
 */
export function handleDeleteArtifact(
  artifact: ArtifactModel,
  { onSuccess, onError }: IOHandlerCallback
): void {
  logStore.$patch({
    confirmation: {
      type: ConfirmationType.INFO,
      title: `Delete ${artifact.name}?`,
      body: `Are you sure you would like to delete this artifact?`,
      statusCallback: (isConfirmed: boolean) => {
        if (!isConfirmed) return;

        deleteArtifact(artifact)
          .then(() => {
            selectionStore.clearSelections();
            artifactStore.deleteArtifacts([artifact]);
            onSuccess?.();
          })
          .catch(onError);
      },
    },
  });
}
