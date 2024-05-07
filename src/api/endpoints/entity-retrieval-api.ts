import { ArtifactSchema, ProjectSchema, TraceLinkSchema } from "@/types";
import { buildRequest } from "@/api/util";

/**
 * Gets a specific version of a project.
 *
 * @param versionId - The project version ID to get.
 * @return The matching project.
 */
export async function getProjectVersion(
  versionId: string
): Promise<ProjectSchema> {
  return buildRequest<ProjectSchema, "versionId">("version", {
    versionId,
  }).get();
}

/**
 * Returns the list of artifacts in the given version.
 *
 * @param versionId - The version whose artifacts are returned.
 * @return The list of artifacts.
 */
export async function getArtifactsInVersion(
  versionId: string
): Promise<ArtifactSchema[]> {
  return buildRequest<ArtifactSchema[], "versionId">("artifacts", {
    versionId,
  }).get();
}

/**
 * Returns the list of trace links in the given version.
 *
 * @param versionId - The version whose trace links are returned.
 * @return The list of trace links.
 */
export async function getTracesInVersion(
  versionId: string
): Promise<TraceLinkSchema[]> {
  return buildRequest<TraceLinkSchema[], "versionId">("traces", {
    versionId,
  }).get();
}
