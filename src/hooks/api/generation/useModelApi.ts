import { defineStore } from "pinia";

import {
  IOHandlerCallback,
  ModelShareType,
  GenerationModelSchema,
} from "@/types";
import { useApi, logStore, modelSaveStore, projectStore } from "@/hooks";
import { pinia } from "@/plugins";
import {
  createModel,
  deleteModel,
  getProjectModels,
  shareModel,
} from "@/api/endpoints";

export const useModelApi = defineStore("modelApi", () => {
  const modelApi = useApi("modelApi");

  /**
   * Loads models for the current project.
   */
  async function handleReload(): Promise<void> {
    await modelApi.handleRequest(async () =>
      projectStore.updateProject({
        models: await getProjectModels(projectStore.projectId),
      })
    );
  }

  /**
   * Saves a model, updates app state, and logs the status.
   *
   * @param callbacks - Callbacks for the request.
   */
  async function handleSave(
    callbacks: IOHandlerCallback<GenerationModelSchema>
  ): Promise<void> {
    const model = modelSaveStore.editedModel;

    await modelApi.handleRequest(
      async () => {
        logStore.onInfo(
          `Model is being saved, you'll receive a notification when it is ready: ${model.name}`
        );

        const createdModel = await createModel(projectStore.projectId, model);

        projectStore.models.push(createdModel);

        return createdModel;
      },
      {
        ...callbacks,
        success: `Model has been saved: ${model.name}.`,
        error: `Unable to save model: ${model.name}`,
      }
    );
  }

  /**
   * Deletes a model, updates app state, and logs the status.
   *
   * @param model - The model to create.
   */
  async function handleDelete(model: GenerationModelSchema): Promise<void> {
    await logStore.confirm(
      "Delete Model",
      `Are you sure you want to delete ${model.name}?`,
      async (isConfirmed) => {
        if (!isConfirmed) return;

        await modelApi.handleRequest(
          async () => {
            await deleteModel(projectStore.projectId, model.id);

            projectStore.updateProject({
              models: projectStore.models.filter(({ id }) => id !== model.id),
            });
          },
          {
            success: `Model has been deleted: ${model.name}`,
            error: `Unable to delete model: ${model.name}`,
          }
        );
      }
    );
  }

  /**
   * Shares a model with another project.
   *
   * @param targetProject - The id of the project to share the model to.
   * @param model - The model to share.
   * @param shareMethod - The method by which to share.
   */
  async function handleShare(
    targetProject: string,
    model: GenerationModelSchema,
    shareMethod: ModelShareType
  ): Promise<void> {
    await modelApi.handleRequest(
      async () => shareModel(targetProject, model, shareMethod),
      {
        success: `Successfully shared model: "${model.name}`,
        error: `Unable to share model: "${model.name}`,
      }
    );
  }

  return {
    handleReload,
    handleSave,
    handleDelete,
    handleShare,
  };
});

export default useModelApi(pinia);
