import { Artifact, ArtifactNameValidationResponse } from "@/types";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api/util";
import { CommitBuilder } from "./commit-builder";
import {
  artifactModule,
  artifactSelectionModule,
  projectModule,
} from "@/store";
import { artifacts } from "@/test-data/test-data";

/**
 * Returns whether the given artifact name already exists.
 *
 * @param versionId - The project version to search within.
 * @param artifactName - The artifact name to search for.
 *
 * @return Whether the artifact name is already taken.
 */
export async function isArtifactNameTaken(
  versionId: string,
  artifactName: string
): Promise<ArtifactNameValidationResponse> {
  return authHttpClient<ArtifactNameValidationResponse>(
    fillEndpoint(Endpoint.isArtifactNameTaken, { versionId, artifactName }),
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
    .save()
    .then(({ artifacts }) => artifacts.removed[0])
    .then((artifact) => projectModule.deleteArtifacts([artifact]));
}

/**
 * Creates a new artifact in the given version.
 *
 * @param versionId - The version that the artifact is stored within.
 * @param artifact - The artifact to create.
 *
 * @return The created artifact.
 */
export async function createArtifact(
  versionId: string,
  artifact: Artifact
): Promise<Artifact[]> {
  return CommitBuilder.withCurrentVersion()
    .withNewArtifact(artifact)
    .save()
    .then(({ artifacts }) => artifacts.added)
    .then(async (artifactsAdded) => {
      await projectModule.addOrUpdateArtifacts(artifactsAdded);
      await artifactSelectionModule.selectArtifact(artifactsAdded[0].id);

      return artifactsAdded;
    });
}

/**
 * Updates artifact to the given version.
 *
 * @param versionId - The version that the artifact is stored within.
 * @param artifact - The artifact to create.
 *
 * @return The created artifact.
 */
export async function updateArtifact(
  versionId: string,
  artifact: Artifact
): Promise<void> {
  return CommitBuilder.withCurrentVersion()
    .withModifiedArtifact(artifact)
    .save()
    .then(({ artifacts }) => artifacts.modified)
    .then(projectModule.addOrUpdateArtifacts);
}
