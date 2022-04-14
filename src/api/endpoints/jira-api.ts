import {
  JiraAccessToken,
  JiraCloudSite,
  JiraProject,
  JiraProjectList,
} from "@/types";
import { logModule, sessionModule } from "@/store";
import { authHttpClient, Endpoint } from "@/api";

/**
 * The formatted scopes of jira permissions being requested.
 */
const scopes = [
  // Current Jira API version:
  "read:jira-work",
  // Upcoming Jira API version:
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
 * Runs a fetch call to the Atlassian API.
 *
 * @param args - The fetch parameters to use.
 * @return The returned data.
 */
async function fetchAtlassian<T>(
  ...args: Parameters<typeof fetch>
): Promise<T> {
  const response = await fetch(...args);
  const resJson = (await response.json()) as T;

  if (!response.ok) {
    logModule.onError("Unable to connect to Atlassian");
    throw Error("Unable to connect to Atlassian");
  } else {
    return resJson;
  }
}

/**
 * Opens an external link to authorize Jira.
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
 * Exchanges an Atlassian access code for a API token.
 *
 * @param accessCode - The access code received from authorizing Jira.
 * @return The Jira access token.
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
 * Exchanges an Atlassian access code for the list of cloud sites associated with the given user.
 *
 * @param accessToken - The access token received from authorizing jira.
 * @return The Jira sites for this user.
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
 * Returns all Jira projects for the given user and cloud site.
 *
 * @param accessToken - The access token received from authorizing Jira.
 * @param cloudId - The Jira cloud id to return projects for.
 * @return The user's projects associated with this cloud.
 */
export async function getJiraProjects(
  accessToken: string,
  cloudId: string
): Promise<JiraProject[]> {
  const projects = await fetchAtlassian<JiraProjectList>(
    `https://api.atlassian.com/ex/jira/${cloudId}/rest/api/3/project/search?expand=insight`,
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

/**
 * Creates a new project based on a Jira project.
 *
 * @param accessToken - The access token received from authorizing Jira.
 * @param cloudId - The Jira cloud id for the current site.
 * @param projectId - The Jira project id to import.
 */
export async function createJiraProject(
  accessToken: string,
  cloudId: string,
  projectId: string
): Promise<void> {
  return authHttpClient<void>(Endpoint.jiraProject, {
    method: "POST",
    body: JSON.stringify({
      cloudId,
      projectId,
      bearerAccessToken: accessToken,
    }),
  });
}
