import {
  IOHandlerCallback,
  ModelShareType,
  GenerationModelSchema,
} from "@/types";
import { logStore, modelSaveStore, projectStore } from "@/hooks";
import {
  createModel,
  deleteModel,
  getProjectModels,
  shareModel,
} from "@/api/endpoints";

/**
 * Loads models for the current project.
 */
export async function handleLoadModels(): Promise<void> {
  projectStore.updateProject({
    models: await getProjectModels(projectStore.projectId),
  });
}

/**
 * Saves a model, updates app state, and logs the status.
 *
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleSaveModel({
  onSuccess,
  onError,
}: IOHandlerCallback<GenerationModelSchema>): void {
  const model = modelSaveStore.editedModel;
  logStore.onInfo(
    `Model is being saved, you'll receive a notification when it is ready: ${model.name}`
  );

  createModel(projectStore.projectId, model)
    .then(() => {
      projectStore.models.push(model);
      logStore.onSuccess(
        `Model has been saved: ${model.name}. Navigate to "Trace Links" -> "Train Models" to train your new model.`
      );
      onSuccess?.(model);
    })
    .catch((e) => {
      logStore.onError(`Unable to create saved: ${model.name}`);
      logStore.onDevError(e.message);
      onError?.(e);
    });
}

/**
 * Deletes a model, updates app state, and logs the status.
 *
 * @param model - The model to create.
 */
export function handleDeleteModel(model: GenerationModelSchema): void {
  logStore.confirm(
    "Delete Model",
    `Are you sure you want to delete ${model.name}?`,
    async (isConfirmed) => {
      if (!isConfirmed) return;

      deleteModel(projectStore.projectId, model.id)
        .then(() => {
          projectStore.updateProject({
            models: projectStore.models.filter(({ id }) => id !== model.id),
          });
          logStore.onSuccess(`Model has been deleted: ${model.name}`);
        })
        .catch((e) => {
          logStore.onError(`Unable to delete model: ${model.name}`);
          logStore.onDevError(e.message);
        });
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
export function handleShareModel(
  targetProject: string,
  model: GenerationModelSchema,
  shareMethod: ModelShareType
): void {
  shareModel(targetProject, model, shareMethod)
    .then(() => {
      logStore.onSuccess(`Successfully shared model: "${model.name}`);
    })
    .catch((e) => {
      logStore.onError(`Unable to share model: "${model.name}`);
      logStore.onDevError(e);
    });
}
