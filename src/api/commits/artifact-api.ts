import { Artifact, NameValidationModel } from "@/types";
import { Endpoint, fillEndpoint, authHttpClient, CommitBuilder } from "@/api";

/**
 * Returns whether the given artifact name already exists.
 *
 * @param versionId - The project version to search within.
 * @param artifactName - The artifact name to search for.
 * @return Whether the artifact name is already taken.
 */
export async function getDoesArtifactExist(
  versionId: string,
  artifactName: string
): Promise<boolean> {
  const res = await authHttpClient<NameValidationModel>(
    fillEndpoint(Endpoint.isArtifactNameTaken, { versionId }),
    { method: "POST", body: JSON.stringify({ artifactName }) }
  );

  return res.artifactExists;
}

/**
 * Deletes artifact in project version specified.
 *
 * @param artifact - The artifact to delete.
 * @return The deleted artifact.
 */
export async function deleteArtifact(artifact: Artifact): Promise<Artifact> {
  return CommitBuilder.withCurrentVersion()
    .withRemovedArtifact(artifact)
    .save()
    .then(({ artifacts }) => artifacts.removed[0]);
}

/**
 * Creates a new artifact in the given version.
 *
 * @param versionId - The version that the artifact is stored within.
 * @param artifact - The artifact to create.
 * @return The created artifact.
 */
export async function createArtifact(
  versionId: string,
  artifact: Artifact
): Promise<Artifact[]> {
  return CommitBuilder.withCurrentVersion()
    .withNewArtifact(artifact)
    .save()
    .then(({ artifacts }) => artifacts.added);
}

/**
 * Updates artifact to the given version.
 *
 * @param versionId - The version that the artifact is stored within.
 * @param artifact - The artifact to updated.
 * @return The updated artifact.
 */
export async function updateArtifact(
  versionId: string,
  artifact: Artifact
): Promise<Artifact[]> {
  return CommitBuilder.withCurrentVersion()
    .withModifiedArtifact(artifact)
    .save()
    .then(({ artifacts }) => artifacts.modified);
}
