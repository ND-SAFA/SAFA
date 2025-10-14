/**
 * Defines a 3rd party data installation to a project.
 */
export interface InstallationSchema {
  /**
   * The Jira project ID, or GitHub repository name.
   */
  installationId: string;
  /**
   * The Jira or GitHub organization id that the project is within.
   */
  installationOrgId: string;
  /**
   * The ISO timestamp of the last installation sync.
   */
  lastUpdate: string;
  /**
   * The type of installation.
   */
  type: "GITHUB" | "JIRA";
}
