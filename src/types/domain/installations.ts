/**
 * Defines a 3rd party data installation to a project.
 */
export interface InstallationModel {
  /**
   * The id of the installed data source.
   */
  installationId: string;
  /**
   * The ISO timestamp of the last installation sync.
   */
  lastUpdate: string;
  /**
   * The type of installation.
   */
  type: "GITHUB" | "JIRA";
}
