import { GitHubImportSchema, GitHubProjectSchema, JobSchema } from "@/types";
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
      `scope=${scopes}`
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
  return true; // TODO: delete
  return (
    (await authHttpClient<boolean | null>(Endpoint.githubValidateCredentials, {
      method: "GET",
    })) === true
  );
}

/**
 * Checks if the saved GitHub credentials are valid.
 *
 * @return Whether the credentials are valid.
 */
export async function refreshGitHubCredentials(): Promise<boolean> {
  return (
    (await authHttpClient<boolean | null>(Endpoint.githubEditCredentials, {
      method: "PUT",
    })) === true
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
  return [
    {
      id: "test",
      name: "Test",
      description: "Test desc",
      size: 0,
      creationDate: "2021-01-01T00:00:00.000Z",
      owner: "test",
      branches: ["master", "dev"],
      defaultBranch: "master",
    },
  ]; // TODO: delete
  return (
    (await authHttpClient<GitHubProjectSchema[]>(Endpoint.githubGetProjects, {
      method: "GET",
    })) || []
  );
}

/**
 * Creates a new project based on a GitHub project.
 *
 * @param owner - The owner of the repository to create a project from.
 * @param repositoryName - The repository to create a project from.
 * @param configuration - The configuration to use for the integration.
 * @return The created import job.
 */
export async function createGitHubProject(
  owner: string,
  repositoryName: string,
  configuration?: GitHubImportSchema
): Promise<JobSchema> {
  return await authHttpClient<JobSchema>(
    fillEndpoint(Endpoint.githubCreateProject, {
      owner,
      repositoryName,
    }),
    {
      method: "POST",
      body: JSON.stringify(configuration),
    }
  );
}

/**
 * Synchronizes the state of GitHub artifacts in a project.
 *
 * @param versionId - The project version to sync data with.
 * @param owner - The owner of the repository to sync a project from.
 * @param repositoryName - The repository to create a project from.
 * @param configuration - The configuration to use for the sync.
 * @return The created import job.
 */
export async function createGitHubProjectSync(
  versionId: string,
  owner: string,
  repositoryName: string,
  configuration?: GitHubImportSchema
): Promise<JobSchema> {
  return await authHttpClient<JobSchema>(
    fillEndpoint(Endpoint.githubSyncProject, {
      versionId,
      owner,
      repositoryName,
    }),
    {
      method: "PUT",
      body: JSON.stringify(configuration),
    }
  );
}
