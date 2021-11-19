import { Artifact, ArtifactNameValidationResponse } from "@/types";
import authHttpClient from "@/api/endpoints/auth-http-client";
import { Endpoint, fillEndpoint } from "@/api/endpoints/endpoints";

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
 * @param versionId - The version belonging to the artifact being deleted.
 * @param artifactName - The name of the artifact being deleted.
 *
 */
export async function deleteArtifactBody(
  versionId: string,
  artifactName: string
): Promise<void> {
  return authHttpClient<void>(
    fillEndpoint(Endpoint.deleteArtifact, { versionId, artifactName }),
    { method: "DELETE" }
  );
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
  return authHttpClient<Artifact>(
    fillEndpoint(Endpoint.createOrUpdateArtifact, { versionId }),
    {
      method: "POST",
      body: JSON.stringify(artifact),
    }
  );
}
