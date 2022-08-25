import {
  ArtifactModel,
  ArtifactData,
  ApprovalType,
  TraceLinkModel,
  TraceType,
  IOHandlerCallback,
  FlatTraceLink,
} from "@/types";
import {
  appStore,
  logStore,
  artifactStore,
  projectStore,
  traceStore,
  approvalStore,
} from "@/hooks";
import {
  createLink,
  getGeneratedLinks,
  updateApprovedLink,
  updateDeclinedLink,
  updateUnreviewedLink,
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
 * Creates a new trace link.
 *
 * @param source - The artifact to link from.
 * @param target - The artifact to link to.
 */
export async function handleCreateLink(
  source: ArtifactModel | ArtifactData,
  target: ArtifactModel | ArtifactData
): Promise<void> {
  const sourceName =
    "artifactName" in source ? source.artifactName : source.name;
  const targetName =
    "artifactName" in target ? target.artifactName : target.name;

  const traceLink: TraceLinkModel = {
    traceLinkId: "",
    sourceId: source.id,
    sourceName,
    targetId: target.id,
    targetName,
    traceType: TraceType.MANUAL,
    approvalStatus: ApprovalType.APPROVED,
    score: 1,
  };

  try {
    const createdLinks = await createLink(traceLink);

    traceStore.addOrUpdateTraceLinks(createdLinks);
  } catch (e) {
    logStore.onError(
      `Unable to create trace link: ${sourceName} -> ${targetName}`
    );
    logStore.onDevError(String(e));
  }
}

/**
 * Processes link approvals, setting the app state to loading in between, and updating trace links afterwards.
 *
 * @param link - The trace link to process.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export async function handleApproveLink(
  link: TraceLinkModel,
  { onSuccess, onError }: IOHandlerCallback
): Promise<void> {
  const currentStatus = link.approvalStatus;

  linkAPIHandler(link, updateApprovedLink, {
    onSuccess: () => {
      traceStore.addOrUpdateTraceLinks([link]);
      approvalStore.approveLink(link);
      onSuccess?.();
    },
    onError: (e) => {
      link.approvalStatus = currentStatus;
      logStore.onError("Unable to approve this link");
      onError?.(e);
    },
  });
}

/**
 * Processes link declines, setting the app state to loading in between, and updating trace links afterwards.
 *
 * @param link - The trace link to process.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export async function handleDeclineLink(
  link: TraceLinkModel,
  { onSuccess, onError }: IOHandlerCallback
): Promise<void> {
  const currentStatus = link.approvalStatus;

  linkAPIHandler(link, updateDeclinedLink, {
    onSuccess: () => {
      traceStore.deleteTraceLinks([link]);
      approvalStore.declineLink(link);
      onSuccess?.();
    },
    onError: (e) => {
      link.approvalStatus = currentStatus;
      logStore.onError("Unable to decline this link");
      onError?.(e);
    },
  });
}

/**
 * Processes link unreview, setting the app state to loading in between, and updating trace links afterwards.
 *
 * @param link - The trace link to process.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export async function handleUnreviewLink(
  link: TraceLinkModel,
  { onSuccess, onError }: IOHandlerCallback
): Promise<void> {
  const currentStatus = link.approvalStatus;

  linkAPIHandler(link, updateUnreviewedLink, {
    onSuccess: () => {
      approvalStore.resetLink(link);
      onSuccess?.();
    },
    onError: (e) => {
      link.approvalStatus = currentStatus;
      logStore.onError("Unable to reset this link");
      onError?.(e);
    },
  });
}

/**
 * Processes link API functions, setting the app state to loading in between.
 *
 * @param link - The trace link to process.
 * @param linkAPI - The endpoint to call with the link.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
function linkAPIHandler(
  link: TraceLinkModel,
  linkAPI: (traceLink: TraceLinkModel) => Promise<TraceLinkModel[]>,
  { onSuccess, onError }: IOHandlerCallback
): void {
  appStore.onLoadStart();
  linkAPI(link)
    .then(() => onSuccess?.())
    .catch((e) => onError?.(e))
    .finally(() => appStore.onLoadEnd());
}
