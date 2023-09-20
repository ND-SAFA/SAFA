import { defineStore } from "pinia";

import {
  IOHandlerCallback,
  ModelShareType,
  GenerationModelSchema,
  ModelApiHook,
} from "@/types";
import { useApi, logStore, modelSaveStore, projectStore } from "@/hooks";
import { pinia } from "@/plugins";
import {
  createModel,
  deleteModel,
  getProjectModels,
  shareModel,
} from "@/api/endpoints";

/**
 * A hook for managing model API requests.
 */
export const useModelApi = defineStore("modelApi", (): ModelApiHook => {
  const modelApi = useApi("modelApi");

  async function handleReload(): Promise<void> {
    await modelApi.handleRequest(async () =>
      projectStore.updateProject({
        models: await getProjectModels(projectStore.projectId),
      })
    );
  }

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
