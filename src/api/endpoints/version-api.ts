import { ProjectCreationResponse, ProjectVersion } from "@/types";
import authHttpClient from "@/api/endpoints/auth-http-client";
import { Endpoint, fillEndpoint } from "@/api/endpoints/endpoints";

/**
 * Gets a specific version of a project.
 *
 * @param versionId - The project version ID to get.
 *
 * @return The matching project.
 */
export async function getProjectVersion(
  versionId: string
): Promise<ProjectCreationResponse> {
  return authHttpClient<ProjectCreationResponse>(
    fillEndpoint(Endpoint.projectVersion, { versionId }),
    { method: "GET" }
  );
}

/**
 * Gets all versions of the given project.
 *
 * @param projectId - The project ID to return versions of.
 */
export async function getProjectVersions(
  projectId?: string
): Promise<ProjectVersion[]> {
  if (!projectId) {
    throw Error("Undefined project identifier");
  }

  return authHttpClient<ProjectVersion[]>(
    fillEndpoint(Endpoint.getProjectVersions, { projectId }),
    { method: "GET" }
  );
}

/**
 * Returns the current version of the given project.
 *
 * @param projectId - The project ID to return the current version of.
 */
export async function getCurrentVersion(
  projectId?: string
): Promise<ProjectVersion> {
  if (!projectId) {
    throw Error("Undefined project identifier");
  }

  return authHttpClient<ProjectVersion>(
    fillEndpoint(Endpoint.getCurrentVersion, { projectId }),
    { method: "GET" }
  );
}

/**
 * Creates a new major version of the project.
 *
 * @param projectId - The project ID to create a new version of.
 *
 * @return The new project version.
 */
export async function createNewMajorVersion(
  projectId: string
): Promise<ProjectVersion> {
  return authHttpClient<ProjectVersion>(
    fillEndpoint(Endpoint.createNewMajorVersion, { projectId }),
    { method: "POST" }
  );
}

/**
 * Creates a new minor version of the project.
 *
 * @param projectId - The project ID to create a new version of.
 *
 * @return The new project version.
 */
export async function createNewMinorVersion(
  projectId: string
): Promise<ProjectVersion> {
  return authHttpClient<ProjectVersion>(
    fillEndpoint(Endpoint.createNewMinorVersion, { projectId }),
    { method: "POST" }
  );
}

/**
 * Creates a new revision version of the project.
 *
 * @param projectId - The project ID to create a new version of.
 *
 * @return The new project version.
 */
export async function createNewRevisionVersion(
  projectId: string
): Promise<ProjectVersion> {
  return authHttpClient<ProjectVersion>(
    fillEndpoint(Endpoint.createNewRevisionVersion, { projectId }),
    {
      method: "POST",
    }
  );
}

/**
 * Deletes a version of the project.
 *
 * @param versionId - The version ID to delete.
 */
export async function deleteProjectVersion(versionId: string): Promise<void> {
  return authHttpClient<void>(
    fillEndpoint(Endpoint.projectVersion, { versionId }),
    {
      method: "DELETE",
    }
  );
}
