import { IOHandlerCallback, Project } from "@/types";
import { navigateTo, Routes } from "@/router";
import { appModule, logModule } from "@/store";
import {
  createJiraProject,
  saveProject,
  handleSetProject,
  handleUploadProjectVersion,
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
      logModule.onSuccess("Successfully created project.");
      await navigateTo(Routes.ARTIFACT);
      await handleSetProject(res);
      onSuccess?.();
    })
    .catch((e) => {
      logModule.onError("Unable to import project");
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
    .then(async () => {
      logModule.onSuccess("Successfully created project.");
      onSuccess?.();
    })
    .catch((e) => {
      logModule.onError("Unable to create a project from these files");
      logModule.onDevError(e);
      onError?.(e);
    })
    .finally(() => appModule.onLoadEnd());
}

/**
 * Imports a Jira project, sets related app state, and logs the status.
 *
 * @param accessToken - The access token received from authorizing Jira.
 * @param cloudId - The Jira cloud id for the current company.
 * @param projectId - The Jira project id to import.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleImportJiraProject(
  accessToken: string,
  cloudId: string,
  projectId: string,
  { onSuccess, onError }: IOHandlerCallback
): void {
  appModule.onLoadStart();

  createJiraProject(accessToken, cloudId, projectId)
    .then(() => {
      logModule.onSuccess("Jira project has been imported.");
      onSuccess?.();
    })
    .catch((e) => {
      logModule.onError("Unable to import jira project");
      logModule.onDevError(e.message);
      onError?.(e);
    })
    .finally(() => appModule.onLoadEnd());
}
