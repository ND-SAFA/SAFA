/**
 * A hook for calling trace matrix API endpoints.
 */
export interface TraceMatrixApiHook {
  /**
   * Creates traces from the given source to target artifact types.
   *
   * @param sourceTypeName - The source artifact type name.
   * @param targetTypeName - The target artifact type name.
   */
  handleCreate(sourceTypeName: string, targetTypeName: string): Promise<void>;
  /**
   * Removes traces from the given source to target artifact types.
   *
   * @param sourceTypeName - The source artifact type name.
   * @param targetTypeName - The target artifact type name.
   */
  handleDeleteTypes(
    sourceTypeName: string,
    targetTypeName: string
  ): Promise<void>;
}
