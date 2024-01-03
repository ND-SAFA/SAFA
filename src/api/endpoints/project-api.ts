import {
  CreateProjectByJsonSchema,
  IdentifierSchema,
  JobSchema,
  ProjectSchema,
} from "@/types";
import { buildRequest } from "@/api";

/**
 * Creates the given project.
 *
 * @param project - The project to save.
 * @return The saved project.
 */
export async function createProject(
  project: Pick<ProjectSchema, "projectId" | "name" | "description">
): Promise<ProjectSchema> {
  return buildRequest<
    ProjectSchema,
    string,
    Pick<ProjectSchema, "projectId" | "name" | "description">
  >("project").post(project);
}

/**
 * Updates project metadata.
 *
 * @param project - The project to edit.
 * @return The edited project.
 */
export async function editProject(
  project: Pick<ProjectSchema, "projectId" | "name" | "description">
): Promise<ProjectSchema> {
  return buildRequest<
    ProjectSchema,
    string,
    Pick<ProjectSchema, "projectId" | "name" | "description">
  >("project").put(project);
}

export async function createProjectCreationJob(
  payload: CreateProjectByJsonSchema
): Promise<JobSchema> {
  return buildRequest<JobSchema, string, CreateProjectByJsonSchema>(
    "createProjectJob"
  ).post(payload);
}

/**
 * Creates a project from the given flat files.
 *
 * @param formData - Form data containing the project files.
 * @return The created project.
 */
export async function createProjectUploadJob(
  formData: FormData
): Promise<JobSchema> {
  return buildRequest<JobSchema, string, FormData>(
    "createProjectThroughFlatFiles"
  )
    .withFormData()
    .post(formData);
}

createProjectUploadJob.FORM_DATA_NAME = "name";
createProjectUploadJob.FORM_DATA_ORG_ID = "orgId";
createProjectUploadJob.FORM_DATA_TEAM_ID = "teamId";
createProjectUploadJob.FORM_DATA_DESCRIPTION = "description";
createProjectUploadJob.FORM_DATA_SUMMARIZE = "summarize";
createProjectUploadJob.FORM_DATA_FILES = "files";

/**
 * Updates an existing project from the given flat files.
 *
 * @param versionId - The project version to update.
 * @param formData - Form data containing the project files.
 * @return The updated project.
 */
export async function createFlatFileUploadJob(
  versionId: string,
  formData: FormData
): Promise<JobSchema> {
  return buildRequest<JobSchema, "versionId", FormData>(
    "updateProjectThroughFlatFiles",
    { versionId }
  )
    .withFormData()
    .post(formData);
}

createFlatFileUploadJob.FORM_DATA_FILES = "files";
createFlatFileUploadJob.FORM_DATA_REPLACE = "asCompleteSet";

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
  return buildRequest<void, "projectId">("updateProject", {
    projectId,
  }).delete();
}
