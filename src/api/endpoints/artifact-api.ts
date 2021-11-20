import { Artifact, ArtifactNameValidationResponse, Commit } from "@/types";
import authHttpClient from "@/api/endpoints/auth-http-client";
import { Endpoint, fillEndpoint } from "@/api/endpoints/endpoints";
import { CommitBuilder } from "@/util/commit-builder";

/**
 * Returns whether the given artifact name already exists.
 *
 * @param projectId - The project to search within.
 * @param artifactName - The artifact name to search for.
 *
 * @return Whether the artifact name is already taken.
 */
export async function isArtifactNameTaken(
  projectId: string,
  artifactName: string
): Promise<ArtifactNameValidationResponse> {
  return authHttpClient<ArtifactNameValidationResponse>(
    fillEndpoint(Endpoint.isArtifactNameTaken, { projectId, artifactName }),
    { method: "GET" }
  );
}

/**
 * Deletes artifact body in project version specified.
 *
 * @param artifact - The artifact to delete.
 *
 */
export async function deleteArtifactBody(artifact: Artifact): Promise<void> {
  return CommitBuilder.withCurrentVersion()
    .withRemovedArtifact(artifact)
    .save();
}

/**
 * Creates a new artifact in the given version.
 *
 * @param versionId - The version that the artifact is stored within.
 * @param artifact - The artifact to create.
 *
 * @return The created artifact.
 */
export async function createOrUpdateArtifact(
  versionId: string,
  artifact: Artifact
): Promise<Artifact> {
  return CommitBuilder.withCurrentVersion()
    .withNewArtifact(artifact)
    .save()
    .then(() => artifact);
}
