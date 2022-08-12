import {
  GitHubInstallationModel,
  GitHubInstallationListModel,
  GitHubRepositoryModel,
  GitHubRepositoryListModel,
  GitHubCredentialsModel,
} from "@/types";

/**
 * The formatted scopes of GitHub permissions being requested.
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
 * Runs a fetch call to the GitHub API using form data and returning params.
 *
 * @param data - The data to include in the body.
 * @param args - The fetch parameters to use.
 * @return The returned data.
 */
async function fetchGitHubForm(
  data: Record<string, string>,
  ...args: Parameters<typeof fetch>
): Promise<URLSearchParams> {
  const body = new FormData();

  Object.entries(data).forEach(([key, val]) => body.append(key, val));

  const res = await fetch(args[0], {
    ...args[1],
    body,
  });

  const params = new URLSearchParams(await res.text());

  if (params.get("error")) {
    throw new Error(
      params.get("error_description") || "Unable to connect to GitHub."
    );
  }

  return params;
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
): Promise<GitHubCredentialsModel> {
  const params = await fetchGitHubForm(
    {
      code: accessCode,
      client_id: process.env.VUE_APP_GITHUB_CLIENT_ID || "",
      client_secret: process.env.VUE_APP_GITHUB_CLIENT_SECRET || "",
      redirect_uri: process.env.VUE_APP_GITHUB_REDIRECT_LINK || "",
    },
    "https://github.com/login/oauth/access_token",
    {
      method: "POST",
    }
  );

  return {
    accessToken: params.get("access_token") || "",
    refreshToken: params.get("refresh_token") || "",
  };
}

/**
 * Exchanges a GitHub refresh token for an API token.
 *
 * @param refreshToken - The refresh token received from GitHub.
 * @return The GitHub access token.
 */
export async function getGitHubRefreshToken(
  refreshToken: string
): Promise<GitHubCredentialsModel> {
  const params = await fetchGitHubForm(
    {
      grant_type: "refresh_token",
      refresh_token: refreshToken,
      client_id: process.env.VUE_APP_GITHUB_CLIENT_ID || "",
      client_secret: process.env.VUE_APP_GITHUB_CLIENT_SECRET || "",
    },
    "https://github.com/login/oauth/access_token",
    {
      method: "POST",
    }
  );

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
): Promise<GitHubInstallationModel[]> {
  const items = await fetchGitHub<GitHubInstallationListModel>(
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
): Promise<GitHubRepositoryModel[]> {
  const { repositories } = await fetchGitHub<GitHubRepositoryListModel>(
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
