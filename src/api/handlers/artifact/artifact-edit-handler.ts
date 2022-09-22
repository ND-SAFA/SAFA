import { ArtifactModel, IOHandlerCallback } from "@/types";
import { artifactStore, logStore, projectStore } from "@/hooks";
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

      logStore.onSuccess(`Edited artifact: ${artifact.name}`);
    } else {
      const createdArtifacts = await createArtifact(versionId, artifact);

      artifactStore.addCreatedArtifact(createdArtifacts[0]);

      logStore.onSuccess(`Created a new artifact: ${artifact.name}`);

      if (parentArtifact) {
        for (const createdArtifact of createdArtifacts) {
          await handleCreateLink(createdArtifact, parentArtifact);
        }
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
  logStore.confirm(
    "Delete Artifact",
    `Are you sure you would like to delete "${artifact.name}"?`,
    async (isConfirmed: boolean) => {
      if (!isConfirmed) return;

      deleteArtifact(artifact)
        .then(() => {
          artifactStore.deleteArtifacts([artifact]);
          logStore.onSuccess(`Deleted artifact: ${artifact.name}`);
          onSuccess?.();
        })
        .catch((e) => {
          logStore.onError(`Unable to delete artifact: ${artifact.name}`);
          onError?.(e);
        });
    }
  );
}
