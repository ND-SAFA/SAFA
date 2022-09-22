import { ConfirmationType, IOHandlerCallback, TrainedModel } from "@/types";
import { logStore, projectStore } from "@/hooks";
import { createModel, deleteModel, getProjectModels } from "@/api/endpoints";

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
 * @param model - The model to create.
 * @param isUpdate - If true, this model already exists and is being updated.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleSaveModel(
  model: TrainedModel,
  isUpdate: boolean,
  { onSuccess, onError }: IOHandlerCallback<TrainedModel>
): void {
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
export function handleDeleteModel(model: TrainedModel): void {
  logStore.$patch({
    confirmation: {
      type: ConfirmationType.INFO,
      title: "Delete Model",
      body: `Are you sure you want to delete ${model.name}?`,
      statusCallback: (isConfirmed: boolean) => {
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
      },
    },
  });
}
