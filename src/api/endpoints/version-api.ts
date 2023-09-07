import { VersionSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Gets all versions of the given project.
 *
 * @param projectId - The project to return versions of.
 * @return All project versions.
 */
export async function getProjectVersions(
  projectId: string
): Promise<VersionSchema[]> {
  return buildRequest<VersionSchema[], "projectId">("getProjectVersions")
    .withParam("projectId", projectId)
    .get();
}

/**
 * Returns the current version of the given project.
 *
 * @param projectId - The project to return the current version of.
 * @return The current version.
 */
export async function getCurrentVersion(
  projectId: string
): Promise<VersionSchema> {
  return buildRequest<VersionSchema, "projectId">("getCurrentVersion")
    .withParam("projectId", projectId)
    .get();
}

/**
 * Creates a new major version of the project.
 *
 * @param projectId - The project to create a new version of.
 * @return The new project version.
 */
export async function createMajorVersion(
  projectId: string
): Promise<VersionSchema> {
  return buildRequest<VersionSchema, "projectId">("createNewMajorVersion")
    .withParam("projectId", projectId)
    .post();
}

/**
 * Creates a new minor version of the project.
 *
 * @param projectId - The project to create a new version of.
 * @return The new project version.
 */
export async function createMinorVersion(
  projectId: string
): Promise<VersionSchema> {
  return buildRequest<VersionSchema, "projectId">("createNewMinorVersion")
    .withParam("projectId", projectId)
    .post();
}

/**
 * Creates a new revision version of the project.
 *
 * @param projectId - The project to create a new version of.
 * @return The new project version.
 */
export async function createRevisionVersion(
  projectId: string
): Promise<VersionSchema> {
  return buildRequest<VersionSchema, "projectId">("createNewRevisionVersion")
    .withParam("projectId", projectId)
    .post();
}

/**
 * Deletes a version of the project.
 *
 * @param versionId - The version ID to delete.
 */
export async function deleteProjectVersion(versionId: string): Promise<void> {
  return buildRequest<void, "versionId">("projectVersion")
    .withParam("versionId", versionId)
    .delete();
}
