import { ProjectSchema } from "@/types";

/**
 * A hook for calling set project API endpoints.
 */
export interface SetProjectApiHook {
  /**
   * Moves user to the document if one is set by currentDocumentId.
   * Otherwise, default document would continue to be in view.
   *
   * @param project The project possibly containing a currentDocumentId.
   */
  handleSetCurrentDocument(project: ProjectSchema): Promise<void>;
  /**
   * Clears project store data.
   */
  handleClear(): Promise<void>;
  /**
   * Sets a newly created project.
   *
   * @param project - Project created containing entities.
   */
  handleSet(project: ProjectSchema): Promise<void>;
  /**
   * Reloads the current project.
   */
  handleReload(): Promise<void>;
}
