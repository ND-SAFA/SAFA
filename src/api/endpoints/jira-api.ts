import {
  InternalJiraCredentials,
  JiraAccessToken,
  JiraCloudSite,
  JiraProject,
  JiraProjectList,
  Job,
} from "@/types";
import { sessionModule } from "@/store";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * The formatted scopes of Jira permissions being requested.
 */
const scopes = encodeURI(
  [
    // Current Jira API version:
    "read:jira-work",
    "read:jira-user",
    "offline_access",
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
  ].join(" ")
);
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
    throw Error("Unable to connect to Atlassian.");
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
 * Exchanges an Atlassian access code for an API token.
 *
 * @param accessCode - The access code received from authorizing Jira.
 * @return The Jira access token.
 */
export async function getJiraToken(
  accessCode: string
): Promise<JiraAccessToken> {
  return fetchAtlassian<JiraAccessToken>(
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
}

/**
 * Exchanges an Atlassian refresh token for an auth token.
 *
 * @param refreshToken - The atlassian refresh token.
 * @return The Jira access token.
 */
export async function getJiraRefreshToken(
  refreshToken: string
): Promise<JiraAccessToken> {
  return fetchAtlassian<JiraAccessToken>(
    "https://auth.atlassian.com/oauth/token",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        refresh_token: refreshToken,
        grant_type: "refresh_token",
        client_id: process.env.VUE_APP_JIRA_CLIENT_ID,
        client_secret: process.env.VUE_APP_JIRA_CLIENT_SECRET,
      }),
    }
  );
}

/**
 * Exchanges an Atlassian access code for the list of cloud sites associated with the given user.
 *
 * @param accessToken - The access token received from authorizing Jira.
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
 * TODO: update to internal GET `/projects/jira/{cloudId}`
 *
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
 * Saves a user's Jira credentials and primary organization.
 *
 * @param credentials - The access and refresh token received from authorizing Jira.
 */
export async function saveJiraCredentials(
  credentials: InternalJiraCredentials
): Promise<void> {
  return authHttpClient<void>(Endpoint.jiraCredentials, {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}

/**
 * Creates a new project based on a Jira project.
 *
 * @param cloudId - The Jira cloud id for this project.
 * @param projectId - The Jira project id to import.
 */
export async function createJiraProject(
  cloudId: string,
  projectId: string
): Promise<Job> {
  return authHttpClient<Job>(
    fillEndpoint(Endpoint.jiraProject, { cloudId, projectId }),
    {
      method: "POST",
    }
  );
}
