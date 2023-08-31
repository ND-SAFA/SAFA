/**
 * A hook for calling artifact search API endpoints.
 */
export interface SearchApiHook {
  /**
   * Handles searching a project, and updating the UI to display the search results.
   */
  handleSearch(): Promise<void>;
}
