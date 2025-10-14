/**
 * Represents a Jira installation (authorized organization).
 */
export interface JiraOrganizationSchema {
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

/**
 * Defines a Jira project import.
 */
export interface JiraImportSchema {
  /**
   * The organization to import to.
   */
  orgId: string;
  /**
   * The team to import to.
   */
  teamId: string;
}
