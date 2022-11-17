import {
  GitHubProjectModel,
  InstallationModel,
  IOHandlerCallback,
  JiraProjectModel,
  URLParameter,
} from "@/types";
import { logStore, projectStore } from "@/hooks";
import {
  getGitHubCredentials,
  getGitHubProjects,
  getJiraCredentials,
  getJiraProjects,
  refreshGitHubCredentials,
  refreshJiraCredentials,
  saveGitHubCredentials,
  saveJiraCredentials,
  getProjectInstallations,
  createGitHubProjectSync,
  createJiraProjectSync,
  handleJobSubmission,
} from "@/api";

/**
 * Handles loading installations affiliated with the current project.
 *
 * @param onComplete - Called once the action is complete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleLoadInstallations({
  onSuccess,
  onError,
  onComplete,
}: IOHandlerCallback): void {
  getProjectInstallations(projectStore.projectId)
    .then((installations) => {
      projectStore.installations = installations;
      onSuccess?.();
    })
    .catch(onError)
    .finally(onComplete);
}

/**
 * Syncs the current project with the selected installation's data.
 *
 * @param installation - The installation to sync data with.
 * @param onComplete - Called once the action is complete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export async function handleSyncInstallation(
  installation: InstallationModel,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  try {
    if (installation.type === "GITHUB") {
      const job = await createGitHubProjectSync(
        projectStore.versionId,
        installation.installationId
      );

      await handleJobSubmission(job);
    } else if (installation.type === "JIRA") {
      const job = await createJiraProjectSync(
        projectStore.versionId,
        installation.installationId
      );

      await handleJobSubmission(job);
    } else {
      throw new Error("Unknown installation type");
    }

    logStore.onSuccess(
      `Integration data is being synced: ${installation.installationId}. 
       You'll receive a notification once data has completed syncing.`
    );
    onSuccess?.();
  } catch (e) {
    logStore.onError(`Unable to sync integration data: ${e}`);
    onError?.(e as Error);
  } finally {
    onComplete?.();
  }
}

/**
 * Handles Jira authentication when the app loads.
 *
 * @param accessCode -The Jira access code, if one exists.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleAuthorizeJira(
  accessCode: URLParameter,
  { onSuccess, onError }: IOHandlerCallback
): void {
  if (accessCode) {
    saveJiraCredentials(String(accessCode)).then(onSuccess).catch(onError);
  } else {
    getJiraCredentials()
      .then(async (valid) => {
        if (!valid) {
          await refreshJiraCredentials();
        }
      })
      .then(onSuccess)
      .catch(onError);
  }
}

/**
 * Loads Jira projects and sets the currently selected cloud id.
 *
 * @param onSuccess - Called if the action is successful, with the jira project list.
 * @param onError - Called if the action fails.
 */
export function handleLoadJiraProjects({
  onSuccess,
  onError,
}: IOHandlerCallback<JiraProjectModel[]>): void {
  getJiraProjects()
    .then(onSuccess)
    .catch((e) => {
      onError?.(e);
      logStore.onError(e);
    });
}

/**
 * Handles GitHub authentication when the app loads.
 *
 * @param accessCode -The GitHub access code, if one exists.
 * @param onSuccess - Called if the action is successful, with the GitHub authorization token.
 * @param onError - Called if the action fails.
 */
export function handleAuthorizeGitHub(
  accessCode: URLParameter,
  { onSuccess, onError }: IOHandlerCallback
): void {
  if (accessCode) {
    saveGitHubCredentials(String(accessCode)).then(onSuccess).catch(onError);
  } else {
    getGitHubCredentials()
      .then(async (valid) => {
        if (!valid) {
          await refreshGitHubCredentials();
        }
      })
      .then(onSuccess)
      .catch(onError);
  }
}

/**
 * Loads GitHub projects and sets the currently selected cloud id.
 *
 * @param credentials - The access and refresh token received from authorizing GitHub.
 * @param onSuccess - Called if the action is successful, with the jira project list.
 * @param onError - Called if the action fails.
 */
export function handleLoadGitHubProjects({
  onSuccess,
  onError,
}: IOHandlerCallback<GitHubProjectModel[]>): void {
  getGitHubProjects()
    .then(onSuccess)
    .catch((e) => {
      onError?.(e);
      logStore.onError(e);
    });
}
