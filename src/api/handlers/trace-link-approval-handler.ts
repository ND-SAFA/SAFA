import {
  ArtifactModel,
  ArtifactData,
  ApprovalType,
  TraceLinkModel,
  TraceType,
  IOHandlerCallback,
  GeneratedLinksModel,
  FlatTraceLink,
} from "@/types";
import { appModule, artifactModule, logModule, projectModule } from "@/store";
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
}: IOHandlerCallback<GeneratedLinksModel>): Promise<void> {
  if (!projectModule.isProjectDefined) return;

  const links: FlatTraceLink[] = [];
  const approved: string[] = [];
  const declined: string[] = [];

  try {
    appModule.onLoadStart();

    const generatedLinks = await getGeneratedLinks(projectModule.versionId);

    generatedLinks.forEach((link) => {
      const source = artifactModule.getArtifactById(link.sourceId);
      const target = artifactModule.getArtifactById(link.targetId);

      if (link.approvalStatus === ApprovalType.APPROVED) {
        approved.push(link.traceLinkId);
      } else if (link.approvalStatus === ApprovalType.DECLINED) {
        declined.push(link.traceLinkId);
      }

      links.push({
        ...link,
        sourceType: source?.type || "",
        sourceBody: source?.body || "",
        targetType: target?.type || "",
        targetBody: target?.body || "",
      });
    });

    onSuccess?.({
      links,
      approved,
      declined,
    });
  } catch (e) {
    onError?.(e);
  } finally {
    appModule.onLoadEnd();
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

    await projectModule.addOrUpdateTraceLinks(createdLinks);
  } catch (e) {
    logModule.onError(
      `Unable to create trace link: ${sourceName} -> ${targetName}`
    );
    logModule.onDevError(e);
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
    onSuccess: async () => {
      await projectModule.addOrUpdateTraceLinks([link]);
      onSuccess?.();
    },
    onError: (e) => {
      link.approvalStatus = currentStatus;
      logModule.onError("Unable to approve this link");
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
    onSuccess: async () => {
      await projectModule.deleteTraceLinks([link]);
      onSuccess?.();
    },
    onError: (e) => {
      link.approvalStatus = currentStatus;
      logModule.onError("Unable to decline this link");
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
      onSuccess?.();
    },
    onError: (e) => {
      link.approvalStatus = currentStatus;
      logModule.onError("Unable to reset this link");
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
  appModule.onLoadStart();
  linkAPI(link)
    .then(() => onSuccess?.())
    .catch((e) => onError?.(e))
    .finally(() => appModule.onLoadEnd());
}
