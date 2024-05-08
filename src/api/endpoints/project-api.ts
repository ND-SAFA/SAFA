import {
  CreateProjectByJsonSchema,
  IdentifierSchema,
  JobSchema,
  ProjectSchema,
  ProjectUploadFormData,
  TransferProjectSchema,
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
    "jobProjects"
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

  return buildRequest<JobSchema, string, FormData>("jobProjectsUpload")
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

  return buildRequest<JobSchema, "versionId", FormData>("jobProjectsVersion", {
    versionId,
  })
    .withFormData()
    .post(formData);
}

/**
 * Returns all project identifiers.
 *
 * @return All project identifiers.
 */
export async function getProjects(): Promise<IdentifierSchema[]> {
  return buildRequest<IdentifierSchema[]>("projectCollection").get();
}

/**
 * Returns all project identifiers for a given team.
 *
 * @return Team's project identifiers.
 */
export async function getTeamProjects(
  teamId: string
): Promise<IdentifierSchema[]> {
  return buildRequest<IdentifierSchema[], "teamId">("projectTeam", {
    teamId,
  }).get();
}

/**
 * Deletes a project.
 *
 * @param projectId - The project ID to delete.
 */
export async function deleteProject(projectId: string): Promise<void> {
  return buildRequest<void, "projectId">("project", {
    projectId,
  }).delete();
}

/**
 * Transfers the ownership of a project.
 *
 * @param projectId - The project ID to transfer.
 * @param newOwner - The new owner of the project.
 * @return The updated project identifier.
 */
export async function setProjectOwner(
  projectId: string,
  newOwner: TransferProjectSchema
): Promise<IdentifierSchema> {
  return buildRequest<IdentifierSchema, "projectId", TransferProjectSchema>(
    "projectTransfer",
    {
      projectId,
    }
  ).put(newOwner);
}
