import { Artifact, TraceApproval, TraceLink } from "@/types";
import { appModule, projectModule } from "@/store";
import { approveLink, declineLink } from "@/api/link-api";
import { createOrUpdateArtifact, deleteArtifact } from "@/api";

/**
 * Creates or updates artifact in BEND then updates app state.
 *
 * @param versionId - The version that the artifact is stored within.
 * @param artifact - The artifact to create.
 *
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
 * Deletes artifact in BEND then deletes artifact from app state.
 *
 * @param projectId - The project whose artifact is going to be deleted.
 * @param artifactName - The name of the artifact to delete.
 *
 */
export function deleteArtifactHandler(
  projectId: string,
  artifactName: string
): Promise<void> {
  return new Promise((resolve, reject) => {
    deleteArtifact(projectId, artifactName)
      .then(() => {
        projectModule.DELETE_ARTIFACT_BY_NAME(artifactName);
        resolve();
      })
      .catch(reject);
  });
}
