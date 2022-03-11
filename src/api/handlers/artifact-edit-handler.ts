import { Artifact, ConfirmationType, TraceApproval, TraceType } from "@/types";
import {
  artifactSelectionModule,
  logModule,
  projectModule,
  viewportModule,
} from "@/store";
import {
  createArtifact,
  createLink,
  deleteArtifactBody,
  updateArtifact,
} from "@/api/commits";
import { getTraceId } from "@/util";

/**
 * Creates or updates artifact in BEND then updates app state.
 *
 * @param versionId - The version that the artifact is stored within.
 * @param artifact - The artifact to create.
 * @param isUpdate - Whether this operation should label this commit as
 * updating a previously existing artifact.
 * @param parentArtifact - The parent artifact to link to.
 */
export async function createOrUpdateArtifactHandler(
  versionId: string,
  artifact: Artifact,
  isUpdate: boolean,
  parentArtifact?: Artifact
): Promise<void> {
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
      await createLink({
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
 * Requests the deletion of artifact body in currently selected project version.
 * The artifact is removed from the store if the request is successful.
 *
 * @param artifact  - The artifact to delete.
 */
export function deleteArtifactFromCurrentVersion(
  artifact: Artifact
): Promise<void> {
  return new Promise((resolve, reject) => {
    if (!projectModule.versionIdWithLog) {
      return resolve();
    }

    logModule.SET_CONFIRMATION_MESSAGE({
      type: ConfirmationType.INFO,
      title: `Delete ${artifact.name}?`,
      body: `Deleting this artifact cannot be undone in this version of SAFA.`,
      statusCallback: (isConfirmed: boolean) => {
        if (isConfirmed) {
          deleteArtifactBody(artifact)
            .then(() => projectModule.deleteArtifacts([artifact]))
            .then(resolve)
            .catch(reject);
        }
      },
    });
  });
}
