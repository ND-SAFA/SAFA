import { ComputedRef } from "vue/dist/vue";
import { WritableComputedRef } from "vue";
import {
  ArtifactSchema,
  ViewSchema,
  ViewType,
  IOHandlerCallback,
} from "@/types";

/**
 * A hook for calling document API endpoints.
 */
export interface DocumentApiHook {
  /**
   * Whether any document request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * The current loaded document.
   * - Reactively loads the current document when set.
   */
  currentDocument: WritableComputedRef<ViewSchema>;
  /**
   * Creates a new document and updates app state.
   *
   * @param name - The document name create.
   * @param type - The document type create.
   * @param artifactIds - The artifacts shown in the document.
   */
  handleCreate(
    name: string,
    type: ViewType,
    artifactIds: string[]
  ): Promise<void>;
  /**
   * Creates a new document from an existing document and updates app state.
   *
   * @param document - The document to create.
   * @param callbacks - The callbacks to call on success, error, and complete.
   */
  handleCreatePreset(
    document: ViewSchema,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Updates an existing document and updates app state.
   *
   * @param document - The document to edit.
   */
  handleUpdate(document: ViewSchema): Promise<void>;
  /**
   * Deletes the document and updates app state.
   * Switches documents if the current one has been deleted.
   *
   * @param callbacks - The callbacks to call on success, error, and complete.
   */
  handleDelete(callbacks: IOHandlerCallback): void;
  /**
   * Updates the artifact for the all documents.
   *
   * @param versionId - The project version to load documents for.
   * @param artifacts - The full list of artifacts.
   */
  handleReload(versionId?: string, artifacts?: ArtifactSchema[]): Promise<void>;
  /**
   * Creates or updates a document, updates app state, and logs the result.
   *
   * @param callbacks - The callbacks to call on success, error, and complete.
   */
  handleSave(callbacks: IOHandlerCallback): Promise<void>;
  /**
   * Switches documents and updates the currently saved document.
   *
   * @param document - The current document.
   */
  handleSwitch(document: ViewSchema): Promise<void>;
}
