import {
  JiraImportSchema,
  JiraOrganizationSchema,
  JiraProjectSchema,
  JobSchema,
} from "@/types";
import { buildRequest } from "@/api";

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
  await buildRequest<void, "accessCode">("jiraCreateCredentials", {
    accessCode,
  }).post();
}

/**
 * Checks if the saved Jira credentials are valid.
 *
 * @return Whether the credentials are valid.
 */
export async function getJiraCredentials(): Promise<boolean> {
  return (
    (
      await buildRequest<{ payload: boolean | null }>(
        "jiraValidateCredentials"
      ).get()
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
      await buildRequest<{ payload: boolean | null }>(
        "jiraEditCredentials"
      ).put()
    ).payload === true
  );
}

/**
 * Deletes the stored Jira credentials.
 */
export async function deleteJiraCredentials(): Promise<void> {
  await buildRequest("jiraEditCredentials").delete();
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
      await buildRequest<{ payload: JiraOrganizationSchema[] }>(
        "jiraGetInstallations"
      ).get()
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
      await buildRequest<{ payload: JiraProjectSchema[] }, "cloudId">(
        "jiraGetProjects",
        { cloudId }
      ).get()
    ).payload || []
  );
}

/**
 * Creates a new project based on a Jira project.
 *
 * @param cloudId - The Jira installation to import projects from.
 * @param id - The Jira project id to import.
 * @param configuration - The configuration for the import.
 * @return The created import job.
 */
export async function createJiraProject(
  cloudId: string,
  id: string,
  configuration: JiraImportSchema
): Promise<JobSchema> {
  return (
    await buildRequest<
      { payload: JobSchema },
      "cloudId" | "id",
      JiraImportSchema
    >("jiraCreateProject", { id, cloudId }).post(configuration)
  ).payload;
}

/**
 * Synchronizes the state of Jira artifacts in a project.
 *
 * @param versionId - The project version to sync.
 * @param cloudId - The Jira installation to import projects from.
 * @param id - The Jira project id to import.
 * @param isNew - Whether or not this is a new installation.
 * @return The created import job.
 */
export async function createJiraProjectSync(
  versionId: string,
  cloudId: string,
  id: string,
  isNew?: boolean
): Promise<JobSchema> {
  const endpoint = buildRequest<
    { payload: JobSchema },
    "versionId" | "cloudId" | "id"
  >("jiraSyncProject", { versionId, id, cloudId });

  return (await (isNew ? endpoint.post() : endpoint.put())).payload;
}
