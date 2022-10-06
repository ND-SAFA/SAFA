import { GitHubRepositoryModel, JobModel } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * The formatted scopes of GitHub permissions being requested.
 */
const scopes = encodeURI(["repo"].join(","));

/**
 * Opens an external link to authorize GitHub.
 */
export function authorizeGitHub(): void {
  window.open(
    `https://github.com/login/oauth/authorize?` +
      `client_id=${process.env.VUE_APP_GITHUB_CLIENT_ID}&` +
      `redirect_uri=${process.env.VUE_APP_GITHUB_REDIRECT_LINK}&` +
      `scopes=${scopes}`
  );
}

/**
 * TODO
 *
 * Save an GitHub access code.
 *
 * @param accessCode - The access code received from authorizing GitHub.
 */
export async function saveGitHubCredentials(
  accessCode: string
  // eslint-disable-next-line @typescript-eslint/no-empty-function
): Promise<void> {}

/**
 * TODO
 *
 * Checks if the saved GitHub credentials are valid.
 */
export async function getGitHubCredentials(): Promise<boolean> {
  return false;
}

/**
 * TODO
 *
 * Gets the list of authorized repositories from GitHub.
 *
 * @return The GitHub repositories for this user.
 */
export async function getGitHubProjects(): Promise<GitHubRepositoryModel[]> {
  return [];
}

/**
 * Creates a new project based on a GitHub project.
 *
 * @param repositoryName - The repository to create a project from.
 * @return The created import job.
 */
export async function createGitHubProject(
  repositoryName: string
): Promise<JobModel> {
  return (
    await authHttpClient<{ payload: JobModel }>(
      fillEndpoint(Endpoint.githubCreateProject, { repositoryName }),
      {
        method: "POST",
      }
    )
  ).payload;
}

/**
 * Synchronizes the state of GitHub artifacts in a project.
 *
 * @param versionId - The project version to sync.
 * @param repositoryName - The repository to create a project from.
 * @return The created import job.
 */
export async function createGitHubProjectSync(
  versionId: string,
  repositoryName: string
): Promise<JobModel> {
  return (
    await authHttpClient<{ payload: JobModel }>(
      fillEndpoint(Endpoint.githubSyncProject, { versionId, repositoryName }),
      {
        method: "PUT",
      }
    )
  ).payload;
}

/**
 * TODO
 *
 * Gets the stored GitHub project information for a specific project.
 *
 * @param projectId - The project to get GitHub credentials for.
 */
export async function getJiraProject(
  projectId: string
): Promise<{ repositoryName: string }> {
  return { repositoryName: "" };
}
