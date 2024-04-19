import { ArtifactHealthSchema, ArtifactSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Get the health checks for an artifact.
 * @param versionId - The unique identifier of the version.
 * @param artifactId - The unique identifier of the artifact.
 * @returns The health checks for the artifact.
 */
export async function getArtifactHealth(
  versionId: string,
  artifactId: string
): Promise<ArtifactHealthSchema> {
  return buildRequest<ArtifactHealthSchema, "versionId" | "artifactId">(
    "getHealthChecks",
    { versionId, artifactId }
  ).get();
}

/**
 * Generate health checks for an artifact.
 * @param versionId - The unique identifier of the version.
 * @param artifact - The artifact to generate health checks for.
 * @returns The health checks for the artifact.
 */
export function generateArtifactHealth(
  versionId: string,
  artifact: ArtifactSchema
): Promise<ArtifactHealthSchema> {
  return buildRequest<ArtifactHealthSchema, "versionId", ArtifactSchema>(
    "generateHealthChecks",
    { versionId }
  ).post(artifact);
}
