/**
 * Represents a GitHub installation (authorized organization).
 */
export interface GitHubOrganizationSchema {
  /**
   * The installation's unique id.
   */
  id: string;
  /**
   * The installation's name.
   */
  name: string;
}

/**
 * Defines a GitHub repository.
 */
export interface GitHubProjectSchema {
  /**
   * The project's id.
   */
  id: number;
  /**
   * The project's name.
   */
  name: string;
  /**
   * The project's description.
   */
  description: string;
  /**
   * The project's url.
   */
  html_url?: string;
  /**
   * The project's size.
   */
  size: number;
  /**
   * A timestamp for the project was created.
   */
  created_at: string;
}
