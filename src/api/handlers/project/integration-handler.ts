import {
  GitHubProjectModel,
  IOHandlerCallback,
  JiraProjectModel,
  URLParameter,
} from "@/types";
import { logStore } from "@/hooks";
import {
  getGitHubCredentials,
  getGitHubProjects,
  getJiraCredentials,
  getJiraProjects,
  refreshGitHubCredentials,
  refreshJiraCredentials,
  saveGitHubCredentials,
  saveJiraCredentials,
} from "@/api";

/**
 * Handles Jira authentication when the app loads.
 *
 * @param accessCode -The Jira access code, if one exists.
 * @param onSuccess - Called if the action is successful, with the Jira authorization token.
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
