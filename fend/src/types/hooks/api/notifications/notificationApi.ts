/**
 * A hook for calling notification API endpoints.
 */
export interface NotificationApiHook {
  /**
   * Connects and subscribes to the given project and version.
   *
   * @param projectId - The project ID to connect to.
   * @param versionId - The project version ID to connect to.
   */
  handleSubscribeVersion(projectId: string, versionId: string): Promise<void>;
}
