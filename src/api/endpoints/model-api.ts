import { ModelShareType, GenerationModelSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Returns the models for the given project.
 *
 * @param projectId - The id of the project to get models for.
 * @return The project's models.
 */
export async function getProjectModels(
  projectId: string
): Promise<GenerationModelSchema[]> {
  return buildRequest<GenerationModelSchema[], "projectId">("getModels", {
    projectId,
  }).get();
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
  model: GenerationModelSchema
): Promise<GenerationModelSchema> {
  return buildRequest<
    GenerationModelSchema,
    "projectId",
    GenerationModelSchema
  >("createModel", { projectId }).post(model);
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
  model: GenerationModelSchema
): Promise<GenerationModelSchema> {
  return buildRequest<
    GenerationModelSchema,
    "projectId" | "modelId",
    GenerationModelSchema
  >("editModel", { projectId, modelId: model.id }).put(model);
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
  return buildRequest<void, "projectId" | "modelId">("deleteModel", {
    projectId,
    modelId,
  }).delete();
}

/**
 * Shares a model with another project.
 *
 * @param targetProject - The id of the project to share the model to.
 * @param model - The model to share.
 * @param shareMethod - The method by which to share.
 */
export async function shareModel(
  targetProject: string,
  model: GenerationModelSchema,
  shareMethod: ModelShareType
): Promise<void> {
  await buildRequest<
    void,
    string,
    {
      model: GenerationModelSchema;
      targetProject: string;
      shareMethod: ModelShareType;
    }
  >("shareModel").post({
    model,
    targetProject,
    shareMethod,
  });
}
