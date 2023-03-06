import { JiraOrganizationSchema, JiraProjectSchema, JobSchema } from "@/types";
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
    (
      await authHttpClient<{ payload: boolean | null }>(
        Endpoint.jiraValidateCredentials,
        {
          method: "GET",
        }
      )
    ).payload === true
  );
}

/**
 * Checks if the saved Jira credentials are valid.
 *
 * @return Whether the credentials are valid.
 */
export async function refreshJiraCredentials(): Promise<boolean> {
  return (
    (
      await authHttpClient<{ payload: boolean | null }>(
        Endpoint.jiraEditCredentials,
        {
          method: "PUT",
        }
      )
    ).payload === true
  );
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
 * Gets Jira installations.
 *
 * @return The user's installations.
 */
export async function getJiraInstallations(): Promise<
  JiraOrganizationSchema[]
> {
  return (
    (
      await authHttpClient<{ payload: JiraOrganizationSchema[] }>(
        Endpoint.jiraGetInstallations,
        {
          method: "GET",
        }
      )
    ).payload || []
  );
}

/**
 * Gets Jira projects for an organization.
 *
 * @param cloudId - The Jira installation to get projects for.
 * @return The user's projects.
 */
export async function getJiraProjects(
  cloudId: string
): Promise<JiraProjectSchema[]> {
  return (
    (
      await authHttpClient<{ payload: JiraProjectSchema[] }>(
        fillEndpoint(Endpoint.jiraGetProjects, { cloudId }),
        {
          method: "GET",
        }
      )
    ).payload || []
  );
}

/**
 * Creates a new project based on a Jira project.
 *
 * @param cloudId - The Jira installation to import projects from.
 * @param id - The Jira project id to import.
 * @return The created import job.
 */
export async function createJiraProject(
  cloudId: string,
  id: string
): Promise<JobSchema> {
  return (
    await authHttpClient<{ payload: JobSchema }>(
      fillEndpoint(Endpoint.jiraCreateProject, { cloudId, id }),
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
 * @param cloudId - The Jira installation to import projects from.
 * @param id - The Jira project id to import.
 */
export async function createJiraProjectSync(
  versionId: string,
  cloudId: string,
  id: string
): Promise<JobSchema> {
  return (
    await authHttpClient<{ payload: JobSchema }>(
      fillEndpoint(Endpoint.jiraSyncProject, { versionId, cloudId, id }),
      {
        method: "PUT",
      }
    )
  ).payload;
}
