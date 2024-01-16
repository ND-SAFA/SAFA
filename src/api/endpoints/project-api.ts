import {
  CreateProjectByJsonSchema,
  IdentifierSchema,
  JobSchema,
  ProjectSchema,
  ProjectUploadFormData,
  VersionUploadFormData,
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
 * @param uploadData - Form data containing the project files.
 * @return The created project.
 */
export async function createProjectUploadJob(
  uploadData: ProjectUploadFormData
): Promise<JobSchema> {
  const formData = new FormData();

  formData.append("name", uploadData.name);
  formData.append("orgId", uploadData.orgId);
  formData.append("teamId", uploadData.teamId);
  formData.append("description", uploadData.description);
  formData.append("summarize", uploadData.summarize.toString());
  uploadData.files.forEach((file: File) => {
    formData.append("files", file);
  });

  return buildRequest<JobSchema, string, FormData>(
    "createProjectThroughFlatFiles"
  )
    .withFormData()
    .post(formData);
}

/**
 * Updates an existing project from the given flat files.
 *
 * @param versionId - The project version to update.
 * @param uploadData - Form data containing the project files.
 * @return The updated project.
 */
export async function createFlatFileUploadJob(
  versionId: string,
  uploadData: VersionUploadFormData
): Promise<JobSchema> {
  const formData = new FormData();

  formData.append("asCompleteSet", uploadData.asCompleteSet.toString());
  uploadData.files.forEach((file: File) => {
    formData.append("files", file);
  });

  return buildRequest<JobSchema, "versionId", FormData>(
    "updateProjectThroughFlatFiles",
    { versionId }
  )
    .withFormData()
    .post(formData);
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
  return buildRequest<void, "projectId">("updateProject", {
    projectId,
  }).delete();
}
