import {
  DeltaPayload,
  Project,
  ProjectCreationResponse,
  ProjectIdentifier,
  ProjectVersion,
} from "@/types";
import authHttpClient from "@/api/endpoints/auth-http-client";
import { Endpoint, fillEndpoint } from "@/api/endpoints/endpoints";

/**
 * Creates a new project from the given flat files.
 *
 * @param formData - Form data containing the project files.
 *
 * @return The created project.
 */
export async function createProjectFromFlatFiles(
  formData: FormData
): Promise<ProjectCreationResponse> {
  return authHttpClient<ProjectCreationResponse>(
    Endpoint.createProjectFromFlatFiles,
    {
      method: "POST",
      body: formData,
    },
    false
  );
}

/**
 * Updates an existing project from the given flat files.
 *
 * @param versionId - The project version to update.
 * @param formData - Form data containing the project files.
 *
 * @return The updated project.
 */
export async function updateProjectThroughFlatFiles(
  versionId: string,
  formData: FormData
): Promise<ProjectCreationResponse> {
  return authHttpClient<ProjectCreationResponse>(
    fillEndpoint(Endpoint.updateProjectThroughFlatFiles, { versionId }),
    {
      method: "POST",
      body: formData,
    },
    false
  );
}

/**
 * Saves or updates the given project.
 *
 * @param project - The project to save.
 *
 * @return The saved project.
 */
export async function saveOrUpdateProject(
  project: Project
): Promise<ProjectCreationResponse> {
  return authHttpClient<ProjectCreationResponse>(Endpoint.project, {
    method: "POST",
    body: JSON.stringify(project),
  });
}

/**
 * Returns all project identifiers.
 *
 * @return All project identifiers.
 */
export async function getProjects(): Promise<ProjectIdentifier[]> {
  return authHttpClient<ProjectIdentifier[]>(Endpoint.project, {
    method: "GET",
  });
}

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
 * Deletes a project.
 *
 * @param projectId - The project ID to delete.
 */
export async function deleteProject(projectId: string): Promise<void> {
  return authHttpClient<void>(
    fillEndpoint(Endpoint.updateProject, { projectId }),
    {
      method: "DELETE",
    }
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

/**
 * Generates the delta between two project versions.
 *
 * @param sourceVersionId - The source version of the project.
 * @param targetVersionId - The target version of the project.
 *
 * @return The delta from the source to the target versions.
 */
export async function getProjectDelta(
  sourceVersionId: string,
  targetVersionId: string
): Promise<DeltaPayload> {
  return authHttpClient<DeltaPayload>(
    fillEndpoint(Endpoint.getProjectDelta, {
      sourceVersionId,
      targetVersionId,
    }),
    {
      method: "GET",
    }
  );
}
