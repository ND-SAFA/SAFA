import {
  CreateProjectByJsonSchema,
  IOHandlerCallback,
  ProjectSchema,
} from "@/types";
import { appStore, integrationsStore, logStore, projectStore } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import {
  createGitHubProject,
  createJiraProject,
  createProjectCreationJob,
  handleJobSubmission,
  handleLoadVersion,
  handleUploadProjectVersion,
  saveProject,
} from "@/api";

/**
 * Creates a new project, sets related app state, and logs the status.
 *
 * @param projectCreationRequest - The project to create and requests to generate trace links.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleImportProject(
  projectCreationRequest: CreateProjectByJsonSchema,
  { onSuccess, onError }: IOHandlerCallback
): void {
  const name = projectCreationRequest.project.name;

  appStore.onLoadStart();

  createProjectCreationJob(projectCreationRequest)
    .then(async (job) => {
      await handleJobSubmission(job);
      await navigateTo(Routes.UPLOAD_STATUS);
      logStore.onSuccess(`Project is being created: ${name}`);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError(`Unable to import project: ${name}`);
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
    ProjectSchema,
    "projectId" | "name" | "description" | "projectVersion"
  >,
  files: File[],
  { onSuccess, onError }: IOHandlerCallback
): void {
  appStore.onLoadStart();

  saveProject(project)
    .then(async (project) => {
      if (files.length === 0) {
        logStore.onSuccess(`Project has been created: ${project.name}`);
        projectStore.addProject(project);
        await handleLoadVersion(project.projectVersion?.versionId || "");
      } else {
        await handleUploadProjectVersion(
          project.projectId,
          project.projectVersion?.versionId || "",
          files,
          true
        );
      }
    })
    .then(onSuccess)
    .catch(onError)
    .finally(() => appStore.onLoadEnd());
}

/**
 * Imports a Jira project, sets related app state, and moves to the upload page.
 *
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleImportJiraProject({
  onSuccess,
  onError,
}: IOHandlerCallback): void {
  const projectId = integrationsStore.jiraProject?.id;

  if (!projectId) return;

  appStore.onLoadStart();

  createJiraProject(projectId)
    .then(async (job) => {
      await handleJobSubmission(job);
      integrationsStore.jiraProject = undefined;
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
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleImportGitHubProject({
  onSuccess,
  onError,
}: IOHandlerCallback): void {
  const repositoryName = integrationsStore.gitHubProject?.name;

  if (!repositoryName) return;

  appStore.onLoadStart();

  createGitHubProject(repositoryName)
    .then(async (job) => {
      await handleJobSubmission(job);
      integrationsStore.gitHubProject = undefined;
      logStore.onSuccess(`GitHub project has been created: ${repositoryName}`);
      await navigateTo(Routes.UPLOAD_STATUS);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError(`GitHub to import jira project: ${repositoryName}`);
      logStore.onDevError(e.message);
      onError?.(e);
    })
    .finally(() => appStore.onLoadEnd());
}
