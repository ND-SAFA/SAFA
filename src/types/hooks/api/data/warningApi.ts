/**
 * A hook for calling warning API endpoints.
 */
export interface WarningApiHook {
  /**
   * Call this function whenever warnings need to be re-downloaded.
   *
   * @param versionId - The project version to load from.
   */
  handleReload(versionId: string): Promise<void>;
}
