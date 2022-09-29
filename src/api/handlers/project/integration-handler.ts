import {
  GitHubCredentialsModel,
  GitHubRepositoryModel,
  InternalGitHubCredentialsModel,
  InternalJiraCredentialsModel,
  IOHandlerCallback,
  JiraAccessTokenModel,
  JiraProjectModel,
  LocalStorageKeys,
  URLParameter,
} from "@/types";
import { logStore } from "@/hooks";
import {
  getGitHubRefreshToken,
  getGitHubRepositories,
  getGitHubToken,
  getJiraProjects,
  getJiraRefreshToken,
  getJiraToken,
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
  { onSuccess, onError }: IOHandlerCallback<InternalJiraCredentialsModel>
): void {
  const handleSuccess = (token: JiraAccessTokenModel) => {
    localStorage.setItem(
      LocalStorageKeys.JIRA_REFRESH_TOKEN,
      token.refresh_token
    );

    onSuccess?.({
      bearerAccessToken: token.access_token,
      refreshToken: token.refresh_token,
      cloudId: localStorage.getItem(LocalStorageKeys.JIRA_CLOUD_ID) || "",
      clientId: process.env.VUE_APP_JIRA_CLIENT_ID || "",
      clientSecret: process.env.VUE_APP_JIRA_CLIENT_SECRET || "",
    });
  };

  if (accessCode) {
    getJiraToken(String(accessCode)).then(handleSuccess).catch(onError);
  } else {
    const refreshToken =
      localStorage.getItem(LocalStorageKeys.JIRA_REFRESH_TOKEN) || "";

    getJiraRefreshToken(refreshToken).then(handleSuccess).catch(onError);
  }
}

/**
 * Loads Jira projects and sets the currently selected cloud id.
 *
 * @param credentials - The access and refresh token received from authorizing Jira.
 * @param onSuccess - Called if the action is successful, with the jira project list.
 * @param onError - Called if the action fails.
 */
export function handleLoadJiraProjects(
  credentials: InternalJiraCredentialsModel,
  { onSuccess, onError }: IOHandlerCallback<JiraProjectModel[]>
): void {
  localStorage.setItem(LocalStorageKeys.JIRA_CLOUD_ID, credentials.cloudId);

  saveJiraCredentials(credentials).catch(onError);

  getJiraProjects(credentials.bearerAccessToken, credentials.cloudId)
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
  { onSuccess, onError }: IOHandlerCallback<InternalGitHubCredentialsModel>
): void {
  const handleSuccess = (token: GitHubCredentialsModel) => {
    localStorage.setItem(
      LocalStorageKeys.GIT_HUB_REFRESH_TOKEN,
      token.refreshToken
    );

    onSuccess?.({
      ...token,
      installationId:
        localStorage.getItem(LocalStorageKeys.GIT_HUB_INSTALLATION_ID) || "",
      clientId: process.env.VUE_APP_GITHUB_CLIENT_ID || "",
      clientSecret: process.env.VUE_APP_GITHUB_CLIENT_SECRET || "",
      accessTokenExpiration: Date.now() + 28800000, // 8 hours in ms.
      refreshTokenExpiration: Date.now() + 7776000000, // 90 days in ms.
    });
  };

  if (accessCode) {
    getGitHubToken(String(accessCode)).then(handleSuccess).catch(onError);
  } else {
    const refreshToken =
      localStorage.getItem(LocalStorageKeys.GIT_HUB_REFRESH_TOKEN) || "";

    getGitHubRefreshToken(refreshToken).then(handleSuccess).catch(onError);
  }
}

/**
 * Loads GitHub projects and sets the currently selected cloud id.
 *
 * @param credentials - The access and refresh token received from authorizing GitHub.
 * @param onSuccess - Called if the action is successful, with the jira project list.
 * @param onError - Called if the action fails.
 */
export function handleLoadGitHubProjects(
  credentials: InternalGitHubCredentialsModel,
  { onSuccess, onError }: IOHandlerCallback<GitHubRepositoryModel[]>
): void {
  localStorage.setItem(
    LocalStorageKeys.GIT_HUB_INSTALLATION_ID,
    credentials.installationId
  );

  saveGitHubCredentials(credentials).catch(onError);

  getGitHubRepositories(credentials.accessToken, credentials.installationId)
    .then(onSuccess)
    .catch((e) => {
      onError?.(e);
      logStore.onError(e);
    });
}
