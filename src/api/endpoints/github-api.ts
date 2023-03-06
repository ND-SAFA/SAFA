import { GitHubProjectSchema, JobSchema } from "@/types";
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
 * Save an GitHub access code.
 *
 * @param accessCode - The access code received from authorizing GitHub.
 */
export async function saveGitHubCredentials(accessCode: string): Promise<void> {
  await authHttpClient(
    fillEndpoint(Endpoint.githubCreateCredentials, { accessCode }),
    {
      method: "POST",
    }
  );
}

/**
 * Checks if the saved GitHub credentials are valid.
 *
 * @return Whether the credentials are valid.
 */
export async function getGitHubCredentials(): Promise<boolean> {
  return (
    (
      await authHttpClient<{ payload: boolean | null }>(
        Endpoint.githubValidateCredentials,
        {
          method: "GET",
        }
      )
    ).payload === true
  );
}

/**
 * Checks if the saved GitHub credentials are valid.
 *
 * @return Whether the credentials are valid.
 */
export async function refreshGitHubCredentials(): Promise<boolean> {
  return (
    (
      await authHttpClient<{ payload: boolean | null }>(
        Endpoint.githubEditCredentials,
        {
          method: "PUT",
        }
      )
    ).payload === true
  );
}

/**
 * Deletes the stored GitHub credentials.
 */
export async function deleteGitHubCredentials(): Promise<void> {
  await authHttpClient(Endpoint.githubEditCredentials, {
    method: "DELETE",
  });
}

/**
 * Gets the list of authorized repositories from GitHub.
 *
 * @return The GitHub repositories for this user.
 */
export async function getGitHubProjects(): Promise<GitHubProjectSchema[]> {
  return (
    (
      await authHttpClient<{ payload: GitHubProjectSchema[] }>(
        Endpoint.githubGetProjects,
        {
          method: "GET",
        }
      )
    ).payload || []
  );
}

/**
 * Creates a new project based on a GitHub project.
 *
 * @param repositoryName - The repository to create a project from.
 * @return The created import job.
 */
export async function createGitHubProject(
  repositoryName: string
): Promise<JobSchema> {
  return (
    await authHttpClient<{ payload: JobSchema }>(
      fillEndpoint(Endpoint.githubCreateProject, {
        repositoryName,
      }),
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
): Promise<JobSchema> {
  return (
    await authHttpClient<{ payload: JobSchema }>(
      fillEndpoint(Endpoint.githubSyncProject, {
        versionId,
        repositoryName,
      }),
      {
        method: "PUT",
      }
    )
  ).payload;
}
