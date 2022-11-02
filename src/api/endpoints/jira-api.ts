import { JiraProjectModel, JobModel } from "@/types";
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
 * Opens an external link to authorize Jira.
 */
export function authorizeJira(): void {
  window.open(
    `https://auth.atlassian.com/authorize?` +
      `audience=api.atlassian.com&` +
      `client_id=${process.env.VUE_APP_JIRA_CLIENT_ID}&` +
      `scope=${scopes}&` +
      `redirect_uri=${process.env.VUE_APP_JIRA_REDIRECT_LINK}&` +
      `state=${String(Math.random()).slice(0, 10)}&` +
      `response_type=code&` +
      `prompt=consent`
  );
}

/**
 * Save an Atlassian access code.
 *
 * @param accessCode - The access code received from authorizing Jira.
 */
export async function saveJiraCredentials(accessCode: string): Promise<void> {
  await authHttpClient(
    fillEndpoint(Endpoint.jiraCreateCredentials, { accessCode }),
    {
      method: "POST",
    }
  );
}

/**
 * Checks if the saved Jira credentials are valid.
 *
 * @return Whether the credentials are valid.
 */
export async function getJiraCredentials(): Promise<boolean> {
  return (
    await authHttpClient<{ payload: boolean }>(
      Endpoint.jiraValidateCredentials,
      {
        method: "GET",
      }
    )
  ).payload;
}

/**
 * Checks if the saved Jira credentials are valid.
 *
 * @return Whether the credentials are valid.
 */
export async function refreshJiraCredentials(): Promise<void> {
  await authHttpClient(Endpoint.jiraEditCredentials, {
    method: "PUT",
  });
}

/**
 * Deletes the stored Jira credentials.
 */
export async function deleteJiraCredentials(): Promise<void> {
  await authHttpClient(Endpoint.jiraEditCredentials, {
    method: "DELETE",
  });
}

/**
 * Gets Jira projects for an organization.
 *
 * @return The user's projects.
 */
export async function getJiraProjects(): Promise<JiraProjectModel[]> {
  return (
    await authHttpClient<{ payload: JiraProjectModel[] }>(
      Endpoint.jiraGetProjects,
      {
        method: "GET",
      }
    )
  ).payload;
}

/**
 * Creates a new project based on a Jira project.
 *
 * @param id - The Jira project id to import.
 * @return The created import job.
 */
export async function createJiraProject(id: string): Promise<JobModel> {
  return (
    await authHttpClient<{ payload: JobModel }>(
      fillEndpoint(Endpoint.jiraCreateProject, { id }),
      {
        method: "POST",
      }
    )
  ).payload;
}

/**
 * Synchronizes the state of Jira artifacts in a project.
 *
 * @param versionId - The project version to sync.
 * @param id - The Jira project id to import.
 */
export async function createJiraProjectSync(
  versionId: string,
  id: string
): Promise<JobModel> {
  return (
    await authHttpClient<{ payload: JobModel }>(
      fillEndpoint(Endpoint.jiraSyncProject, { versionId, id }),
      {
        method: "PUT",
      }
    )
  ).payload;
}

/**
 * TODO
 *
 * Gets the stored Jira project information for a specific project.
 *
 * @param projectId - The project to get Jira credentials for.
 */
// export async function getJiraProject(
//   projectId: string
// ): Promise<{ id: string }> {
//   return { id: "" };
// }
