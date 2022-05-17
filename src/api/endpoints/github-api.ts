import {
  GitHubInstallation,
  GitHubInstallationList,
  GitHubRepository,
  GitHubRepositoryList,
  InternalGitHubCredentials,
} from "@/types";

/**
 * The formatted scopes of jira permissions being requested.
 */
const scopes = encodeURI(["repo"].join(","));

/**
 * Runs a fetch call to the GitHub API.
 *
 * @param args - The fetch parameters to use.
 * @return The returned data.
 */
async function fetchGitHub<T>(...args: Parameters<typeof fetch>): Promise<T> {
  const response = await fetch(...args);
  const resJson = (await response.json()) as T;

  if (!response.ok) {
    throw Error("Unable to connect to GitHub.");
  } else {
    return resJson;
  }
}

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
 * Exchanges a GitHub access code for an API token.
 *
 * @param accessCode - The access code received from authorizing GitHub.
 * @return The GitHub access token.
 */
export async function getGitHubToken(
  accessCode: string
): Promise<InternalGitHubCredentials> {
  const data = new FormData();

  data.append("code", accessCode);
  data.append("client_id", process.env.VUE_APP_GITHUB_CLIENT_ID || "");
  data.append("client_secret", process.env.VUE_APP_GITHUB_CLIENT_SECRET || "");
  data.append("redirect_uri", process.env.VUE_APP_GITHUB_REDIRECT_LINK || "");

  const res = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    body: data,
  });

  const params = new URLSearchParams(await res.text());

  if (params.get("error")) {
    throw new Error(
      params.get("error_description") || "Unable to connect to GitHub."
    );
  }

  return {
    accessToken: params.get("access_token") || "",
    refreshToken: params.get("refresh_token") || "",
  };
}

/**
 * Exchanges a GitHub access code for the list of installations associated with the given user.
 *
 * @param accessToken - The access token received from authorizing GitHub.
 * @return The GitHub organizations for this user.
 */
export async function getGitHubInstallations(
  accessToken: string
): Promise<GitHubInstallation[]> {
  const items = await fetchGitHub<GitHubInstallationList>(
    "https://api.github.com/user/installations",
    {
      method: "GET",
      headers: {
        Accept: "application/vnd.github.v3+json",
        Authorization: `token ${accessToken}`,
      },
    }
  );

  return items.installations;
}

/**
 * Returns all GitHub projects for the given user and installation.
 *
 * @param accessToken - The access token received from authorizing GitHub.
 * @param installationId - The GitHub installation id to return projects for.
 * @return The GitHub organizations for this user.
 */
export async function getGitHubRepositories(
  accessToken: string,
  installationId: string
): Promise<GitHubRepository[]> {
  const { repositories } = await fetchGitHub<GitHubRepositoryList>(
    `https://api.github.com/user/installations/${installationId}/repositories`,
    {
      method: "GET",
      headers: {
        Accept: "application/vnd.github.v3+json",
        Authorization: `token ${accessToken}`,
      },
    }
  );

  return repositories;
}
