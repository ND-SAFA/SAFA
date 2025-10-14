import { GitHubImportSchema, GitHubProjectSchema, JobSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * The formatted scopes of GitHub permissions being requested.
 */
const scopes = encodeURI(["repo"].join(","));

/**
 * Opens an external link to authorize GitHub.
 *
 * @param validCredentials - Whether the current credentials are valid.
 */
export function authorizeGitHub(validCredentials: boolean): void {
  if (validCredentials) {
    window.open(
      "https://github.com/settings/connections/applications/8ff9708f3644c2d5fbbe"
    );
  } else {
    window.open(
      `https://github.com/login/oauth/authorize?` +
        `client_id=${process.env.VUE_APP_GITHUB_CLIENT_ID}&` +
        `redirect_uri=${process.env.VUE_APP_GITHUB_REDIRECT_LINK}&` +
        `scope=${scopes}`
    );
  }
}

/**
 * Save an GitHub access code.
 *
 * @param accessCode - The access code received from authorizing GitHub.
 */
export async function saveGitHubCredentials(accessCode: string): Promise<void> {
  await buildRequest<void, "accessCode">("githubCreateCredentials", {
    accessCode,
  }).post();
}

/**
 * Checks if the saved GitHub credentials are valid.
 *
 * @return Whether the credentials are valid.
 */
export async function getGitHubCredentials(): Promise<boolean> {
  return (
    (await buildRequest<boolean | null>("githubValidateCredentials").get()) ===
    true
  );
}

/**
 * Checks if the saved GitHub credentials are valid.
 *
 * @return Whether the credentials are valid.
 */
export async function refreshGitHubCredentials(): Promise<boolean> {
  return (
    (await buildRequest<boolean | null>("githubEditCredentials").put()) === true
  );
}

/**
 * Deletes the stored GitHub credentials.
 */
export async function deleteGitHubCredentials(): Promise<void> {
  await buildRequest("githubEditCredentials").delete();
}

/**
 * Gets the list of authorized repositories from GitHub.
 *
 * @return The GitHub repositories for this user.
 */
export async function getGitHubProjects(): Promise<GitHubProjectSchema[]> {
  return (
    (await buildRequest<GitHubProjectSchema[]>("githubGetProjects").get()) || []
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
  configuration: GitHubImportSchema
): Promise<JobSchema> {
  return buildRequest<
    JobSchema,
    "owner" | "repositoryName",
    GitHubImportSchema | undefined
  >("githubCreateProject", { owner, repositoryName }).post(configuration);
}

/**
 * Synchronizes the state of GitHub artifacts in a project.
 *
 * @param versionId - The project version to sync data with.
 * @param owner - The owner of the repository to sync a project from.
 * @param repositoryName - The repository to create a project from.
 * @param configuration - The configuration to use for the sync.
 * @param isNew - Whether or not this is a new installation.
 * @return The created import job.
 */
export async function createGitHubProjectSync(
  versionId: string,
  owner: string,
  repositoryName: string,
  configuration?: GitHubImportSchema,
  isNew?: boolean
): Promise<JobSchema> {
  const endpoint = buildRequest<
    JobSchema,
    "versionId" | "owner" | "repositoryName",
    GitHubImportSchema | undefined
  >("githubSyncProject", { versionId, owner, repositoryName });

  return isNew ? endpoint.post(configuration) : endpoint.put(configuration);
}
