import { Artifact, ConfirmationType, TraceApproval, TraceType } from "@/types";
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
 * Creates or updates and artifact, and updates app state.
 *
 * @param artifact - The artifact to create.
 * @param isUpdate - Whether this operation should label this commit as
 * updating a previously existing artifact.
 * @param parentArtifact - The parent artifact to link to.
 */
export async function handleSaveArtifact(
  artifact: Artifact,
  isUpdate: boolean,
  parentArtifact?: Artifact
): Promise<void> {
  const versionId = projectModule.versionIdWithLog;

  if (isUpdate) {
    const updatedArtifacts = await updateArtifact(versionId, artifact);

    await projectModule.addOrUpdateArtifacts(updatedArtifacts);
  } else {
    const createdArtifacts = await createArtifact(versionId, artifact);

    await projectModule.addOrUpdateArtifacts(createdArtifacts);
    await artifactSelectionModule.selectArtifact(createdArtifacts[0].id);
    await viewportModule.setArtifactTreeLayout();

    if (!parentArtifact) return;

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
}

/**
 * Deletes an artifact, and updates the app state.
 *
 * @param artifact  - The artifact to delete.
 */
export function handleDeleteArtifact(artifact: Artifact): Promise<void> {
  return new Promise((resolve, reject) => {
    logModule.SET_CONFIRMATION_MESSAGE({
      type: ConfirmationType.INFO,
      title: `Delete ${artifact.name}?`,
      body: `Deleting this artifact cannot be undone in this version of SAFA.`,
      statusCallback: (isConfirmed: boolean) => {
        if (isConfirmed) {
          deleteArtifact(artifact)
            .then(async () => {
              await projectModule.deleteArtifacts([artifact]);
              await artifactSelectionModule.UNSELECT_ARTIFACT();
            })
            .then(resolve)
            .catch(reject);
        }
      },
    });
  });
}
