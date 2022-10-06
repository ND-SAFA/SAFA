import { JiraCloudSiteModel, JiraProjectModel, JobModel } from "@/types";
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
 * TODO
 *
 * Save an Atlassian access code.
 *
 * @param accessCode - The access code received from authorizing Jira.
 */
// eslint-disable-next-line @typescript-eslint/no-empty-function
export async function saveJiraCredentials(accessCode: string): Promise<void> {}

/**
 * TODO
 *
 * Checks if the saved Jira credentials are valid.
 */
export async function getJiraCredentials(): Promise<boolean> {
  return false;
}

/**
 * TODO
 *
 * Gets the list of cloud sites associated with the saved user.
 *
 * @return The Jira sites for this user.
 */
export async function getJiraOrganizations(): Promise<JiraCloudSiteModel[]> {
  return [];
}

/**
 * Gets Jira projects for an organization.
 *
 * @param cloudId - The Jira cloud id to get projects for.
 * @return The created import job.
 */
export async function getJiraProjects(
  cloudId: string
): Promise<JiraProjectModel[]> {
  return (
    await authHttpClient<{ payload: JiraProjectModel[] }>(
      fillEndpoint(Endpoint.jiraGetProjects, { cloudId }),
      {
        method: "GET",
      }
    )
  ).payload;
}

/**
 * Creates a new project based on a Jira project.
 *
 * @param cloudId - The Jira cloud id for this project.
 * @param id - The Jira project id to import.
 * @return The created import job.
 */
export async function createJiraProject(
  cloudId: string,
  id: string
): Promise<JobModel> {
  return (
    await authHttpClient<{ payload: JobModel }>(
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
 * @param cloudId - The Jira cloud id for this project.
 * @param id - The Jira project id to import.
 */
export async function createJiraProjectSync(
  versionId: string,
  cloudId: string,
  id: string
): Promise<JobModel> {
  return (
    await authHttpClient<{ payload: JobModel }>(
      fillEndpoint(Endpoint.jiraSyncProject, { versionId, cloudId, id }),
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
export async function getJiraProject(
  projectId: string
): Promise<{ cloudId: string; id: string }> {
  return { cloudId: "", id: "" };
}
