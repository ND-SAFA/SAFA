import {
  ApprovalType,
  IOHandlerCallback,
  FlatTraceLink,
  TraceLinkModel,
  GeneratedMatrixModel,
} from "@/types";
import {
  appStore,
  artifactStore,
  projectStore,
  approvalStore,
  logStore,
  traceStore,
} from "@/hooks";
import {
  createGeneratedLinks,
  getGeneratedLinks,
  saveGeneratedLinks,
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
  { onSuccess, onError }: IOHandlerCallback<TraceLinkModel[]>
): Promise<void> {
  const generatedLinks: TraceLinkModel[] = [];
  const matricesName = matrices
    .map(({ source, target }) => `${source} -> ${target}`)
    .join(", ");

  try {
    appStore.onLoadStart();

    for (const { source, target, method } of matrices) {
      const sourceArtifacts = artifactStore.getArtifactsByType[source] || [];
      const targetArtifacts = artifactStore.getArtifactsByType[target] || [];
      const traceLinks = await createGeneratedLinks({
        sourceArtifacts,
        targetArtifacts,
        method,
      });
      generatedLinks.push(...traceLinks);
    }

    const createdLinks = await saveGeneratedLinks(generatedLinks);

    traceStore.addOrUpdateTraceLinks(createdLinks);
    logStore.onSuccess(
      `Generated ${createdLinks.length} new trace links: ${matricesName}`
    );
    onSuccess?.(createdLinks);
  } catch (e) {
    logStore.onError(`Unable to generate new trace links: ${matricesName}`);
    onError?.(e as Error);
  } finally {
    appStore.onLoadEnd();
  }
}
