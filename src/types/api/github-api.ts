/**
 * Defines a GitHub repository.
 */
export interface GitHubProjectModel {
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
