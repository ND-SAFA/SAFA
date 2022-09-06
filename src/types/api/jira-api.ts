/**
 * Represents the access code returned from authorizing jira.
 */
export interface JiraAccessTokenModel {
  /**
   * The API bearer access token.
   */
  access_token: string;
  /**
   * The API refresh token.
   */
  refresh_token: string;
}

/**
 * Represents the cloud site returned from authorizing jira.
 */
export interface JiraCloudSiteModel {
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
  /**
   * The Jira site's avatar url.
   */
  avatarUrl: string;
}

/**
 * Represents a jira project.
 */
export interface JiraProjectModel {
  /**
   * The project's domain url.
   */
  self: string;
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
   * The avatar urls for the project.
   */
  avatarUrls: {
    "48x48": string;
    "32x32": string;
    "24x24": string;
    "16x16": string;
  };
  /**
   * Project insights.
   */
  insight: {
    /**
     * The total number of issues in this project.
     */
    totalIssueCount: number;
    /**
     * A timestamp for last time an issue was updated.
     */
    lastIssueUpdateTime: string;
  };
}

/**
 * Represents a list of jira projects.
 */
export interface JiraProjectListModel {
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
  values: JiraProjectModel[];
}

/**
 * Represents the internally stored Jira credentials.
 */
export interface InternalJiraCredentialsModel {
  /**
   * The API bearer access token.
   */
  bearerAccessToken: string;
  /**
   * The API refresh token.
   */
  refreshToken: string;
  /**
   * The Jira cloud id, if one is set.
   */
  cloudId: string;
  /**
   * Our Jira app client id.
   */
  clientId: string;
  /**
   * Our Jira app client secret.
   */
  clientSecret: string;
}
