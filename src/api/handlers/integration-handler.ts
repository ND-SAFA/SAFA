import {
  InternalGitHubCredentials,
  InternalJiraCredentials,
  IOHandlerCallback,
  JiraAccessToken,
  JiraProject,
  LocalStorageKeys,
  URLParameter,
} from "@/types";
import {
  getGitHubToken,
  getJiraProjects,
  getJiraRefreshToken,
  getJiraToken,
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
  { onSuccess, onError }: IOHandlerCallback<InternalJiraCredentials>
): void {
  const handleSuccess = (token: JiraAccessToken) => {
    localStorage.setItem(
      LocalStorageKeys.JIRA_REFRESH_TOKEN,
      token.refresh_token
    );

    onSuccess?.({
      accessToken: token.access_token,
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
 * Handles Jira authentication when the app loads.
 *
 * @param credentials - The access and refresh token received from authorizing Jira.
 * @param onSuccess - Called if the action is successful, with the jira project list.
 * @param onError - Called if the action fails.
 */
export function handleLoadJiraProjects(
  credentials: InternalJiraCredentials,
  { onSuccess, onError }: IOHandlerCallback<JiraProject[]>
): void {
  localStorage.setItem(LocalStorageKeys.JIRA_CLOUD_ID, credentials.cloudId);

  saveJiraCredentials(credentials)
    .then(async () => {
      const projects = await getJiraProjects(
        credentials.accessToken,
        credentials.cloudId
      );

      onSuccess?.(projects);
    })
    .catch(onError);
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
  { onSuccess, onError }: IOHandlerCallback<InternalGitHubCredentials>
): void {
  if (!accessCode) {
    onError?.(new Error("No access code exists."));
    return;
  }

  getGitHubToken(String(accessCode)).then(onSuccess).catch(onError);
}
