import {
  JiraAccessToken,
  JiraCloudSite,
  JiraProject,
  JiraProjectList,
} from "@/types";
import { sessionModule } from "@/store";

const scopes = [
  "read:jira-work",
  // "read:issue-type:jira",
  // "read:project:jira",
  // "read:project.property:jira",
  // "read:user:jira",
  // "read:application-role:jira",
  // "read:avatar:jira",
  // "read:group:jira",
  // "read:issue-type-hierarchy:jira",
  // "read:project-category:jira",
  // "read:project-version:jira",
  // "read:project.component:jira",
]
  .map((scope) => scope.replace(/:/g, "%3A"))
  .join("%20");

/**
 * Runs a fetch call to the atlassian API.
 * @param args - The fetch parameters to use.
 */
async function fetchAtlassian<T>(
  ...args: Parameters<typeof fetch>
): Promise<T> {
  const response = await fetch(...args);

  return (await response.json()) as T;
}

/**
 * Opens an external link to authorize jira.
 */
export function authorizeJira(): void {
  window.open(
    `https://auth.atlassian.com/authorize?` +
      `audience=api.atlassian.com&` +
      `client_id=${process.env.VUE_APP_JIRA_CLIENT_ID}&` +
      `scope=${scopes}&` +
      `redirect_uri=${process.env.VUE_APP_JIRA_REDIRECT_LINK}&` +
      `state=${sessionModule.getToken}&` +
      `response_type=code&` +
      `prompt=consent`
  );
}

/**
 * Exchanges an atlassian access code for a API token.
 *
 * @param accessCode - The access code received from authorizing jira.
 * @return The jira access token.
 */
export async function getJiraToken(accessCode: string): Promise<string> {
  const authorization = await fetchAtlassian<JiraAccessToken>(
    "https://auth.atlassian.com/oauth/token",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        code: accessCode,
        grant_type: "authorization_code",
        client_id: process.env.VUE_APP_JIRA_CLIENT_ID,
        client_secret: process.env.VUE_APP_JIRA_CLIENT_SECRET,
        redirect_uri: process.env.VUE_APP_JIRA_REDIRECT_LINK,
      }),
    }
  );

  return authorization.access_token;
}

/**
 * Exchanges an atlassian access code for a API token.
 *
 * @param accessToken - The access token received from authorizing jira.
 * @return The jira sites for this user.
 */
export async function getJiraCloudSites(
  accessToken: string
): Promise<JiraCloudSite[]> {
  return fetchAtlassian<JiraCloudSite[]>(
    "https://api.atlassian.com/oauth/token/accessible-resources",
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );
}

/**
 * Returns all jira projects for the given user.
 *
 * @param accessToken - The access token received from authorizing jira.
 * @param cloudId - The cloud id for the current user.
 * @return The user's projects associated with this company.
 */
export async function getJiraProjects(
  accessToken: string,
  cloudId: string
): Promise<JiraProject[]> {
  const projects = await fetchAtlassian<JiraProjectList>(
    `https://api.atlassian.com/ex/jira/${cloudId}/rest/api/3/project/search`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        Accept: "application/json",
      },
    }
  );

  return projects.values;
}
