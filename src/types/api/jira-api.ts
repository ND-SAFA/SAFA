/**
 * Represents the access code returned from authorizing jira.
 */
export interface JiraAccessToken {
  /**
   * The API bearer access token.
   */
  access_token: string;
}

/**
 * Represents the cloud site returned from authorizing jira.
 */
export interface JiraCloudSite {
  /**
   * The Jira site's id.
   */
  id: string;
  /**
   * The Jira site's name.
   */
  name: string;
  /**
   * The Jira site's url.
   */
  url: string;
}

/**
 * Represents a jira project.
 */
export interface JiraProject {
  /**
   * The project id.
   */
  id: string;
  /**
   * The project name.
   */
  name: string;
}

/**
 * Represents a list of jira projects.
 */
export interface JiraProjectList {
  /**
   * The total results per page.
   */
  maxResults: number;
  /**
   * The starting project number.
   */
  startAt: number;
  /**
   * The total number of projects.
   */
  total: number;
  /**
   * Whether this is the last page.
   */
  isLast: boolean;
  /**
   * The list of projects.
   */
  values: JiraProject[];
}
