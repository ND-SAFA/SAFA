import { Artifact, ConfirmationType } from "@/types";
import { appModule, projectModule } from "@/store";
import {
  createArtifact,
  updateArtifact,
  deleteArtifactBody,
} from "@/api/endpoints";

/**
 * Creates or updates artifact in BEND then updates app state.
 *
 * @param versionId - The version that the artifact is stored within.
 * @param artifact - The artifact to create.
 * @param isUpdate - Whether this operation should label this commit as
 * updating a previously existing artifact.
 */
export function createOrUpdateArtifactHandler(
  versionId: string,
  artifact: Artifact,
  isUpdate: boolean
): Promise<void> {
  return new Promise((resolve, reject) => {
    const artifactPromise = isUpdate ? updateArtifact : createArtifact;
    artifactPromise(versionId, artifact)
      .then(() => {
        projectModule.addOrUpdateArtifacts([artifact]);
      })
      .then(resolve)
      .catch(reject);
  });
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
    const versionId = projectModule.getProject.projectVersion?.versionId;
    if (versionId === undefined) {
      appModule.onWarning(
        "A project version must be selected to delete an artifact."
      );
      return resolve();
    }

    appModule.SET_CONFIRMATION_MESSAGE({
      type: ConfirmationType.INFO,
      title: `Delete ${artifact.name}?`,
      body: `Deleting this artifact cannot be undone in this version of SAFA.`,
      statusCallback: (isConfirmed: boolean) => {
        if (isConfirmed) {
          deleteArtifactBody(artifact)
            .then(() => {
              projectModule.DELETE_ARTIFACT_BY_NAME(artifact.name);
              resolve();
            })
            .catch(reject);
        }
      },
    });
  });
}
