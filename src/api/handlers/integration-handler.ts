import {
  IOHandlerCallback,
  JiraAccessToken,
  JiraProject,
  URLParameter,
} from "@/types";
import {
  getJiraProjects,
  getJiraRefreshToken,
  getJiraToken,
  saveJiraCredentials,
} from "@/api";

/**
 * Handles Jira authentication when the app loads.
 *
 * @param accessCode -The Jira access code, if noe exists.
 * @param onSuccess - Called if the action is successful, with the jira authorization token.
 * @param onError - Called if the action fails.
 */
export function handleAuthorizeJira(
  accessCode: URLParameter,
  { onSuccess, onError }: IOHandlerCallback<JiraAccessToken>
): void {
  if (accessCode) {
    getJiraToken(String(accessCode)).then(onSuccess).catch(onError);
  } else {
    getJiraRefreshToken().then(onSuccess).catch(onError);
  }
}

/**
 * Handles Jira authentication when the app loads.
 *
 * @param token - The access and refresh token received from authorizing Jira.
 * @param cloudId - The Jira cloud id for the current site.
 * @param onSuccess - Called if the action is successful, with the jira project list.
 * @param onError - Called if the action fails.
 */
export function handleLoadJiraProjects(
  token: JiraAccessToken,
  cloudId: string,
  { onSuccess, onError }: IOHandlerCallback<JiraProject[]>
): void {
  saveJiraCredentials(token, cloudId)
    .then(async () => {
      const projects = await getJiraProjects(token.access_token, cloudId);

      onSuccess?.(projects);
    })
    .catch(onError);
}
