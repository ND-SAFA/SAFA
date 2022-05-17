/**
 * Defines the credentials returned by github.
 */
export interface InternalGitHubCredentials {
  /**
   * The API bearer access token.
   */
  accessToken: string;
  /**
   * The API refresh token.
   */
  refreshToken: string;
}

/**
 * Defines a GitHub installation (organization).
 */
export interface GitHubInstallation {
  /**
   * The installation's id.
   */
  id: string;
  /**
   * The installation's name.
   */
  name: string;
  /**
   * The installation's slug id.
   */
  app_slug: string;
  /**
   * The installation's url.
   */
  url: string;
}

/**
 * Defines a list of GitHub installations (organization).
 */
export interface GitHubInstallationList {
  /**
   * The list of installations.
   */
  installations: GitHubInstallation[];
  /**
   * The count of installations.
   */
  total_count: number;
}

/**
 * Defines a GitHub repository.
 */
export interface GitHubRepository {
  /**
   * The project's id.
   */
  id: string;
  /**
   * The project's name.
   */
  name: string;
  /**
   * The project's full name.
   */
  full_name: string;
  /**
   * The project's avatar.
   */
  avatar_url?: string;
  /**
   * The project's url.
   */
  url: string;
  /**
   * The project's size.
   */
  size: number;
  /**
   * A timestamp for the project was created.
   */
  created_at: string;
  /**
   * A timestamp for the project was last updated.
   */
  updated_at: string;
}

/**
 * Defines a list of GitHub repositories.
 */
export interface GitHubRepositoryList {
  /**
   * The list of installations.
   */
  repositories: GitHubRepository[];
  /**
   * The count of installations.
   */
  total_count: number;
}
