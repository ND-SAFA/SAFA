import {
  GenerationModelSchema,
  IOHandlerCallback,
  ModelShareType,
} from "@/types";

/**
 * A hook for calling model API endpoints.
 */
export interface ModelApiHook {
  /**
   * Loads models for the current project.
   */
  handleReload(): Promise<void>;
  /**
   * Saves a model, updates app state, and logs the status.
   *
   * @param callbacks - Callbacks for the request.
   */
  handleSave(
    callbacks: IOHandlerCallback<GenerationModelSchema>
  ): Promise<void>;
  /**
   * Deletes a model, updates app state, and logs the status.
   *
   * @param model - The model to create.
   */
  handleDelete(model: GenerationModelSchema): Promise<void>;
  /**
   * Shares a model with another project.
   *
   * @param targetProject - The id of the project to share the model to.
   * @param model - The model to share.
   * @param shareMethod - The method by which to share.
   */
  handleShare(
    targetProject: string,
    model: GenerationModelSchema,
    shareMethod: ModelShareType
  ): Promise<void>;
}
