import {
  GitHubCredentialsModel,
  InternalGitHubCredentialsModel,
  IOHandlerCallback,
  ProjectModel,
} from "@/types";
import { appStore, logStore } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import {
  createGitHubProject,
  createJiraProject,
  createProjectCreationJob,
  handleJobSubmission,
  handleUploadProjectVersion,
  saveProject,
} from "@/api";

/**
 * Creates a new project, sets related app state, and logs the status.
 *
 * @param project - The project to create.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleImportProject(
  project: ProjectModel,
  { onSuccess, onError }: IOHandlerCallback
): void {
  appStore.onLoadStart();

  createProjectCreationJob(project)
    .then(async (job) => {
      await handleJobSubmission(job);
      await navigateTo(Routes.UPLOAD_STATUS);
      logStore.onSuccess(`Project is being created: ${project.name}`);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError(`Unable to import project: ${project.name}`);
      logStore.onDevError(e);
      onError?.(e);
    })
    .finally(() => appStore.onLoadEnd());
}

/**
 * Creates a new project from files, sets related app state, and logs the status.
 *
 * @param project - The project to create.
 * @param files - The files to upload.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleBulkImportProject(
  project: Pick<
    ProjectModel,
    "projectId" | "name" | "description" | "projectVersion"
  >,
  files: File[],
  { onSuccess, onError }: IOHandlerCallback
): void {
  appStore.onLoadStart();

  saveProject(project)
    .then(async (project) =>
      handleUploadProjectVersion(
        project.projectId,
        project.projectVersion?.versionId || "",
        files,
        true
      )
    )
    .then(onSuccess)
    .catch(onError)
    .finally(() => appStore.onLoadEnd());
}

/**
 * Imports a Jira project, sets related app state, and moves to the upload page.
 *
 * @param cloudId - The Jira cloud id for this project.
 * @param projectId - The Jira project id to import.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleImportJiraProject(
  cloudId: string,
  projectId: string,
  { onSuccess, onError }: IOHandlerCallback
): void {
  appStore.onLoadStart();

  createJiraProject(cloudId, projectId)
    .then(async (job) => {
      await handleJobSubmission(job);
      logStore.onSuccess(`Jira project has been created: ${projectId}`);
      await navigateTo(Routes.UPLOAD_STATUS);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError(`Unable to import jira project: ${projectId}`);
      logStore.onDevError(e.message);
      onError?.(e);
    })
    .finally(() => appStore.onLoadEnd());
}

/**
 * Imports a GitHub project, sets related app state, and moves to the upload page.
 *
 * @param projectId - The GitHub project id to import.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleImportGitHubProject(
  projectId: string,
  { onSuccess, onError }: IOHandlerCallback
): void {
  appStore.onLoadStart();

  createGitHubProject(projectId)
    .then(async (job) => {
      await handleJobSubmission(job);
      logStore.onSuccess(`GitHub project has been created: ${projectId}`);
      await navigateTo(Routes.UPLOAD_STATUS);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError(`GitHub to import jira project: ${projectId}`);
      logStore.onDevError(e.message);
      onError?.(e);
    })
    .finally(() => appStore.onLoadEnd());
}
