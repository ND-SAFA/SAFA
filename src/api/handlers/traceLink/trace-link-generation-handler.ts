import {
  ApprovalType,
  FlatTraceLink,
  GeneratedMatrixModel,
  IOHandlerCallback,
  TrainedModel,
} from "@/types";
import {
  approvalStore,
  appStore,
  artifactStore,
  logStore,
  projectStore,
  traceStore,
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
 * @param matrices - An array of source and target artifact types to generate traces between.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export async function handleGenerateLinks(
  matrices: GeneratedMatrixModel[],
  { onSuccess, onError }: IOHandlerCallback
): Promise<void> {
  const matricesName = matrices
    .map(({ source, target }) => `${source} -> ${target}`)
    .join(", ");

  try {
    for (const { source, target, method, model } of matrices) {
      const sourceArtifacts = artifactStore.getArtifactsByType[source] || [];
      const targetArtifacts = artifactStore.getArtifactsByType[target] || [];
      const job = await createGeneratedLinks({
        sourceArtifacts,
        targetArtifacts,
        method,
        model,
        projectVersion: projectStore.version,
      });

      await handleJobSubmission(job);
    }
    logStore.onInfo(
      `Started generating new trace links: ${matricesName}. You'll receive a notification once they are added.`
    );
    onSuccess?.();
  } catch (e) {
    logStore.onError(`Unable to generate new trace links: ${matricesName}`);
    onError?.(e as Error);
  }
}

/**
 * Trains models on created trace links.
 *
 * @param model - The model to train.
 * @param matrices - An array of source and target artifact types to train on traces between.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export async function handleTrainModel(
  model: TrainedModel,
  matrices: GeneratedMatrixModel[],
  { onSuccess, onError }: IOHandlerCallback
): Promise<void> {
  const matricesName = matrices
    .map(({ source, target }) => `${source} -> ${target}`)
    .join(", ");

  try {
    for (const { source, target } of matrices) {
      const sources = artifactStore.getArtifactsByType[source] || [];
      const targets = artifactStore.getArtifactsByType[target] || [];
      const traces = traceStore.getTraceLinksByArtifactSets(sources, targets, [
        "manual",
        "approved",
      ]);
      const job = await createModelTraining({
        projectId: projectStore.projectId,
        sources,
        targets,
        traces,
        model,
      });

      await handleJobSubmission(job);
    }
    logStore.onInfo(
      `Started training model on: ${matricesName}. You'll receive a notification once complete.`
    );
    onSuccess?.();
  } catch (e) {
    logStore.onError(`Unable to train model on: ${matricesName}`);
    onError?.(e as Error);
  }
}
