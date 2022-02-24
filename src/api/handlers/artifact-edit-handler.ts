import { Artifact, ConfirmationType } from "@/types";
import { logModule, projectModule } from "@/store";
import {
  createArtifact,
  updateArtifact,
  deleteArtifactBody,
} from "@/api/commits";

/**
 * Creates or updates artifact in BEND then updates app state.
 *
 * @param versionId - The version that the artifact is stored within.
 * @param artifact - The artifact to create.
 * @param isUpdate - Whether this operation should label this commit as
 * updating a previously existing artifact.
 */
export async function createOrUpdateArtifactHandler(
  versionId: string,
  artifact: Artifact,
  isUpdate: boolean
): Promise<void> {
  if (isUpdate) {
    await updateArtifact(versionId, artifact);
  } else {
    await createArtifact(versionId, artifact);
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
