/**
 * Represents a jira project.
 */
export interface JiraProjectSchema {
  /**
   * The project's unique id.
   */
  id: string;
  /**
   * The project's unique key name.
   */
  key: string;
  /**
   * The project's name.
   */
  name: string;
  /**
   * The project's description.
   */
  description: string;
  /**
   * The project's avatar.
   */
  mediumAvatarUrl: string;
}
