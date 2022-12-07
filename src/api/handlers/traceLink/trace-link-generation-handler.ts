import {
  ApprovalType,
  ArtifactLevelSchema,
  FlatTraceLink,
  GeneratedMatrixSchema,
  IOHandlerCallback,
  ModelType,
  GenerationModelSchema,
} from "@/types";
import {
  approvalStore,
  appStore,
  artifactStore,
  logStore,
  projectStore,
} from "@/hooks";
import {
  createGeneratedLinks,
  createModelTraining,
  getGeneratedLinks,
  handleJobSubmission,
} from "@/api";

/**
 * Returns all generated links.
 *
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export async function handleGetGeneratedLinks({
  onSuccess,
  onError,
}: IOHandlerCallback): Promise<void> {
  if (!projectStore.isProjectDefined) return;

  const traceLinks: FlatTraceLink[] = [];
  const approvedIds: string[] = [];
  const declinedIds: string[] = [];

  try {
    appStore.onLoadStart();

    const generatedLinks = await getGeneratedLinks(projectStore.versionId);

    generatedLinks.forEach((link) => {
      const source = artifactStore.getArtifactById(link.sourceId);
      const target = artifactStore.getArtifactById(link.targetId);

      if (link.approvalStatus === ApprovalType.APPROVED) {
        approvedIds.push(link.traceLinkId);
      } else if (link.approvalStatus === ApprovalType.DECLINED) {
        declinedIds.push(link.traceLinkId);
      }

      traceLinks.push({
        ...link,
        sourceType: source?.type || "",
        sourceBody: source?.body || "",
        targetType: target?.type || "",
        targetBody: target?.body || "",
      });
    });

    approvalStore.initializeTraces({ traceLinks, approvedIds, declinedIds });

    onSuccess?.();
  } catch (e) {
    onError?.(e as Error);
  } finally {
    appStore.onLoadEnd();
  }
}

/**
 * Generates links between sets of artifact types and adds them to the project.
 *
 * @param method - The base model to generate with.
 * @param model - The model to generate with. Used over the method.
 * @param artifactLevels - An array of source and target artifact types to generate traces between.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
export async function handleGenerateLinks(
  method: ModelType | undefined,
  model: GenerationModelSchema | undefined,
  artifactLevels: ArtifactLevelSchema[],
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  const matricesName = artifactLevels
    .map(({ source, target }) => `${source} -> ${target}`)
    .join(", ");

  try {
    const job = await createGeneratedLinks({
      requests: [createGeneratedMatrix(artifactLevels, method, model)],
      projectVersion: projectStore.version,
    });

    await handleJobSubmission(job);

    logStore.onInfo(
      `Started generating new trace links: ${matricesName}. You'll receive a notification once they are added.`
    );
    onSuccess?.();
  } catch (e) {
    logStore.onError(`Unable to generate new trace links: ${matricesName}`);
    onError?.(e as Error);
  } finally {
    onComplete?.();
  }
}

/**
 * Trains models on created trace links.
 *
 * @param model - The model to train.
 * @param artifactLevels - An array of source and target artifact types to train on traces between.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
export async function handleTrainModel(
  model: GenerationModelSchema,
  artifactLevels: ArtifactLevelSchema[],
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  const matricesName = artifactLevels
    .map(({ source, target }) => `${source} -> ${target}`)
    .join(", ");

  try {
    const job = await createModelTraining(projectStore.projectId, {
      requests: [createGeneratedMatrix(artifactLevels, model.baseModel, model)],
    });

    await handleJobSubmission(job);
    logStore.onInfo(
      `Started training model on: ${matricesName}. You'll receive a notification once complete.`
    );
    onSuccess?.();
  } catch (e) {
    logStore.onError(`Unable to train model on: ${matricesName}`);
    onError?.(e as Error);
  } finally {
    onComplete?.();
  }
}

/**
 * Creates a generated trace matrix defined over many artifact levels for
 * some tracing method or custom model.
 * @param artifactLevels - The artifact levels to train on.
 * @param method - If a baseline method is used, this defines that method.
 * @param model - If a custom model is used,
 */
function createGeneratedMatrix(
  artifactLevels: ArtifactLevelSchema[],
  method?: ModelType,
  model?: GenerationModelSchema
): GeneratedMatrixSchema {
  return {
    method: model?.baseModel || method || ModelType.NLBert,
    model,
    artifactLevels: artifactLevels,
  };
}
