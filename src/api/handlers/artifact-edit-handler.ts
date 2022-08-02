import {
  Artifact,
  ConfirmationType,
  IOHandlerCallback,
  TraceApproval,
  TraceType,
} from "@/types";
import {
  artifactSelectionModule,
  logModule,
  projectModule,
  viewportModule,
} from "@/store";
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
  artifact: Artifact,
  isUpdate: boolean,
  parentArtifact: Artifact | undefined,
  { onSuccess, onError }: IOHandlerCallback
): Promise<void> {
  try {
    const versionId = projectModule.versionIdWithLog;

    if (isUpdate) {
      const updatedArtifacts = await updateArtifact(versionId, artifact);

      await projectModule.addOrUpdateArtifacts(updatedArtifacts);
    } else {
      const createdArtifacts = await createArtifact(versionId, artifact);

      await projectModule.addOrUpdateArtifacts(createdArtifacts);
      artifactSelectionModule.selectArtifact(createdArtifacts[0].id);
      await viewportModule.setArtifactTreeLayout();

      if (!parentArtifact) {
        onSuccess?.();
        return;
      }

      for (const createdArtifact of createdArtifacts) {
        await handleCreateLink({
          traceLinkId: "",
          sourceName: createdArtifact.name,
          sourceId: createdArtifact.id,
          targetName: parentArtifact.name,
          targetId: parentArtifact.id,
          approvalStatus: TraceApproval.APPROVED,
          score: 1,
          traceType: TraceType.MANUAL,
        });
      }
    }

    onSuccess?.();
  } catch (e) {
    logModule.onDevError(e);
    logModule.onError(`Unable to create artifact: ${artifact.name}`);
    onError?.(e);
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
  artifact: Artifact,
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
  artifact: Artifact,
  { onSuccess, onError }: IOHandlerCallback
): Promise<void> {
  return new Promise((resolve, reject) => {
    logModule.SET_CONFIRMATION_MESSAGE({
      type: ConfirmationType.INFO,
      title: `Delete ${artifact.name}?`,
      body: `Deleting this artifact cannot be undone in this version of SAFA.`,
      statusCallback: (isConfirmed: boolean) => {
        if (!isConfirmed) return;

        deleteArtifact(artifact)
          .then(async () => {
            await artifactSelectionModule.UNSELECT_ARTIFACT();
            await projectModule.deleteArtifacts([artifact]);
            onSuccess?.();
            resolve();
          })
          .catch((e) => {
            onError?.(e);
            reject(e);
          });
      },
    });
  });
}
