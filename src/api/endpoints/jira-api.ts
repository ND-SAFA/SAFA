import { sessionModule } from "@/store";

/**
 * Represents the access code returned from authorizing jira.
 */
interface JiraAccessToken {
  access_token: string;
}

/**
 * Represents the cloud id returned from authorizing jira.
 */
interface JiraCloudId {
  id: string;
}

/**
 * Represents a jira project.
 */
interface JiraProject {
  id: string;
  name: string;
}

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
      `client_id=${process.env.JIRA_CLIENT_ID}&` +
      `scope=read%3Ajira-work&` +
      `redirect_uri=${process.env.JIRA_REDIRECT_LINK}&` +
      `state=${sessionModule.getToken}&` +
      `response_type=code&` +
      `prompt=consent`
  );
}

/**
 * Exchanges an atlassian access code for a cloud id.
 *
 * @param accessCode - The access code received from authorizing jira.
 * @return The jira cloud id of the authorized user.
 */
export async function getJiraCloudId(accessCode: string): Promise<string> {
  const authorization = await fetchAtlassian<JiraAccessToken>(
    "https://auth.atlassian.com/oauth/token",
    {
      method: "POST",
      body: JSON.stringify({
        code: accessCode,
        grant_type: "authorization_code",
        client_id: process.env.JIRA_CLIENT_ID,
        client_secret: process.env.JIRA_CLIENT_SECRET,
        redirect_uri: process.env.JIRA_REDIRECT_LINK,
      }),
    }
  );

  const cloudIds = await fetchAtlassian<JiraCloudId[]>(
    "https://api.atlassian.com/oauth/token/accessible-resources",
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${authorization.access_token}`,
      },
    }
  );

  return cloudIds[0]?.id || "";
}

/**
 * Returns all jira projects for the given user.
 *
 * @param cloudId - The cloud id for the current user.
 */
export async function getJiraProjects(cloudId: string): Promise<JiraProject[]> {
  return fetchAtlassian<JiraProject[]>(
    `https://api.atlassian.com/ex/jira/${cloudId}/rest/api/3/project/search`
  );
}
