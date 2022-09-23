import { TrainedModel } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Returns the models for the given project.
 *
 * @param projectId - The id of the project to get models for.
 * @return The project's models.
 */
export async function getProjectModels(
  projectId: string
): Promise<TrainedModel[]> {
  return authHttpClient<TrainedModel[]>(
    fillEndpoint(Endpoint.getModels, {
      projectId,
    }),
    {
      method: "GET",
    }
  );
}

/**
 * Creates a new model.
 *
 * @param projectId - The id of the project to create models for.
 * @param model - The model to create.
 * @return The created model.
 */
export async function createModel(
  projectId: string,
  model: TrainedModel
): Promise<TrainedModel> {
  return authHttpClient<TrainedModel>(
    fillEndpoint(Endpoint.createModel, {
      projectId,
    }),
    {
      method: "POST",
      body: JSON.stringify(model),
    }
  );
}

/**
 * Edits a model.
 *
 * @param projectId - The id of the project to edit the model on.
 * @param model - The edited model.
 * @return The edited model.
 */
export async function editModel(
  projectId: string,
  model: TrainedModel
): Promise<TrainedModel> {
  return authHttpClient<TrainedModel>(
    fillEndpoint(Endpoint.editModel, {
      projectId,
      modelId: model.id,
    }),
    {
      method: "PUT",
      body: JSON.stringify(model),
    }
  );
}

/**
 * Deletes a model.
 *
 * @param projectId - The id of the project to delete the model on.
 * @param modelId - The model id to delete.
 */
export async function deleteModel(
  projectId: string,
  modelId: string
): Promise<void> {
  await authHttpClient<TrainedModel>(
    fillEndpoint(Endpoint.deleteModel, {
      projectId,
      modelId,
    }),
    {
      method: "DELETE",
    }
  );
}
