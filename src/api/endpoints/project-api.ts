import {
  CreateProjectByJsonSchema,
  IdentifierSchema,
  JobSchema,
  ProjectSchema,
} from "@/types";
import { buildRequest } from "@/api";

/**
 * Creates or updates the given project.
 *
 * @param project - The project to save.
 * @return The saved project.
 */
export async function saveProject(
  project: Pick<ProjectSchema, "projectId" | "name" | "description">
): Promise<ProjectSchema> {
  return buildRequest<
    ProjectSchema,
    string,
    Pick<ProjectSchema, "projectId" | "name" | "description">
  >("project").post(project);
}

export async function createProjectCreationJob(
  payload: CreateProjectByJsonSchema
): Promise<JobSchema> {
  return buildRequest<JobSchema, string, CreateProjectByJsonSchema>(
    "createProjectJob"
  ).post(payload);
}

/**
 * Returns all project identifiers.
 *
 * @return All project identifiers.
 */
export async function getProjects(): Promise<IdentifierSchema[]> {
  return buildRequest<IdentifierSchema[]>("project").get();
}

/**
 * Deletes a project.
 *
 * @param projectId - The project ID to delete.
 */
export async function deleteProject(projectId: string): Promise<void> {
  return buildRequest<void, "projectId">("updateProject")
    .withParam("projectId", projectId)
    .delete();
}
