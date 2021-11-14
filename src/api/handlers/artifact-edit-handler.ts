import { Artifact, ConfirmationType } from "@/types";
import { appModule, projectModule } from "@/store";
import { createOrUpdateArtifact, deleteArtifactBody } from "@/api";

/**
 * Creates or updates artifact in BEND then updates app state.
 *
 * @param versionId - The version that the artifact is stored within.
 * @param artifact - The artifact to create.
 */
export function createOrUpdateArtifactHandler(
  versionId: string,
  artifact: Artifact
): Promise<void> {
  return new Promise((resolve, reject) => {
    createOrUpdateArtifact(versionId, artifact)
      .then(() => {
        projectModule.addOrUpdateArtifacts([artifact]);
        resolve();
      })
      .catch(reject);
  });
}

/**
 * Requests the deletion of artifact body in currently selected project version.
 * The artifact is removed from the store if the request is successful.
 *
 * @param artifactName - The name of the artifact to delete.
 */
export function deleteArtifactFromCurrentVersion(
  artifactName: string
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
      title: `Delete ${artifactName}?`,
      body: `Deleting this artifact cannot be undone in this version of SAFA.`,
      statusCallback: (isConfirmed: boolean) => {
        if (isConfirmed) {
          deleteArtifactBody(versionId, artifactName)
            .then(() => {
              projectModule.DELETE_ARTIFACT_BY_NAME(artifactName);
              resolve();
            })
            .catch(reject);
        }
      },
    });
  });
}
