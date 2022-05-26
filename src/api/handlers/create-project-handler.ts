import { InternalGitHubCredentials, IOHandlerCallback, Project } from "@/types";
import { navigateTo, Routes } from "@/router";
import { appModule, logModule } from "@/store";
import {
  createJiraProject,
  handleSetProject,
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
  project: Project,
  { onSuccess, onError }: IOHandlerCallback
): void {
  appModule.onLoadStart();

  saveProject(project)
    .then(async (res) => {
      logModule.onSuccess(`Project has been created: ${project.name}`);
      await navigateTo(Routes.ARTIFACT);
      await handleSetProject(res);
      onSuccess?.();
    })
    .catch((e) => {
      logModule.onError(`Unable to import project: ${project.name}`);
      logModule.onDevError(e);
      onError?.(e);
    })
    .finally(() => appModule.onLoadEnd());
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
  project: Pick<Project, "projectId" | "name" | "description">,
  files: File[],
  { onSuccess, onError }: IOHandlerCallback
): void {
  appModule.onLoadStart();

  saveProject(project)
    .then(async (project) =>
      handleUploadProjectVersion(
        project.project.projectId,
        project.projectVersion.versionId,
        files,
        true
      )
    )
    .then(onSuccess)
    .catch(onError)
    .finally(() => appModule.onLoadEnd());
}

/**
 * Imports a Jira project, sets related app state, and logs the status.
 *
 * @param projectId - The Jira project id to import.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleImportJiraProject(
  projectId: string,
  { onSuccess, onError }: IOHandlerCallback
): void {
  appModule.onLoadStart();

  createJiraProject(projectId)
    .then(async () => {
      logModule.onSuccess(`Jira project has been created: ${projectId}`);
      await navigateTo(Routes.UPLOAD_STATUS);
      onSuccess?.();
    })
    .catch((e) => {
      logModule.onError(`Unable to import jira project: ${projectId}`);
      logModule.onDevError(e.message);
      onError?.(e);
    })
    .finally(() => appModule.onLoadEnd());
}

/**
 * Imports a GitHub project, sets related app state, and logs the status.
 *
 * @param credentials - The access token received from authorizing GitHub.
 * @param orgId - The GitHub organization id for the current company.
 * @param projectId - The GitHub project id to import.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleImportGitHubProject(
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  credentials: InternalGitHubCredentials,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  orgId: string,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  projectId: string,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  { onSuccess, onError }: IOHandlerCallback
): void {
  console.log("Importing from GitHub is not yet enabled.");
}
