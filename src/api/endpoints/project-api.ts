import {
  CreateProjectByJsonSchema,
  IdentifierSchema,
  JobSchema,
  VersionDeltaSchema,
  ProjectSchema,
} from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates or updates the given project.
 *
 * @param project - The project to save.
 * @return The saved project.
 */
export async function saveProject(
  project: Pick<ProjectSchema, "projectId" | "name" | "description">
): Promise<ProjectSchema> {
  return authHttpClient<ProjectSchema>(Endpoint.project, {
    method: "POST",
    body: JSON.stringify(project),
  });
}

export async function createProjectCreationJob(
  payload: CreateProjectByJsonSchema
): Promise<JobSchema> {
  return authHttpClient<JobSchema>(Endpoint.createProjectJob, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/**
 * Returns all project identifiers.
 *
 * @return All project identifiers.
 */
export async function getProjects(): Promise<IdentifierSchema[]> {
  return authHttpClient<IdentifierSchema[]>(Endpoint.project, {
    method: "GET",
  });
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
 * Generates the delta between two project versions.
 *
 * @param sourceVersionId - The source version of the project.
 * @param targetVersionId - The target version of the project.
 * @return The delta from the source to the target versions.
 */
export async function getProjectDelta(
  targetVersionId: string,
  sourceVersionId: string
): Promise<VersionDeltaSchema> {
  return authHttpClient<VersionDeltaSchema>(
    fillEndpoint(Endpoint.getProjectDelta, {
      sourceVersionId,
      targetVersionId,
    }),
    {
      method: "GET",
    }
  );
}
