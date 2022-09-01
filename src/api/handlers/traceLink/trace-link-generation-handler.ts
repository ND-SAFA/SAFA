import {
  ApprovalType,
  IOHandlerCallback,
  FlatTraceLink,
  TraceLinkModel,
} from "@/types";
import {
  appStore,
  artifactStore,
  projectStore,
  approvalStore,
  logStore,
  traceStore,
} from "@/hooks";
import { createGeneratedLinks, createLink, getGeneratedLinks } from "@/api";

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
 * Generates links between two types of artifacts, and adds them to the project.
 *
 * @param sourceType - The source artifact type.
 * @param targetType - The target artifact type.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export async function generateNewLinks(
  sourceType: string,
  targetType: string,
  { onSuccess, onError }: IOHandlerCallback<TraceLinkModel[]>
): Promise<void> {
  try {
    appStore.onLoadStart();

    const sourceArtifacts = artifactStore.getArtifactsByType[sourceType] || [];
    const targetArtifacts = artifactStore.getArtifactsByType[targetType] || [];
    const traceLinks = await createGeneratedLinks(
      sourceArtifacts,
      targetArtifacts
    );
    const createdLinks: TraceLinkModel[] = [];

    for (const traceLink of traceLinks) {
      createdLinks.push(...(await createLink(traceLink)));
    }

    traceStore.addOrUpdateTraceLinks(createdLinks);
    logStore.onSuccess(
      `Generated ${createdLinks.length} new trace links: ${sourceType} -> ${targetType}`
    );
    onSuccess?.(createdLinks);
  } catch (e) {
    logStore.onError(
      `Unable to generate new trace links: ${sourceType} -> ${targetType}`
    );
    onError?.(e as Error);
  } finally {
    appStore.onLoadEnd();
  }
}
