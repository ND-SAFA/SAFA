import {
  ArtifactModel,
  ArtifactData,
  EmptyLambda,
  ApprovalType,
  TraceLinkModel,
  TraceType,
} from "@/types";
import { appModule, logModule, projectModule } from "@/store";
import { createLink, updateApprovedLink, updateDeclinedLink } from "@/api";

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
 * @param onSuccess - Run when the API call successfully resolves.
 */
export async function handleApproveLink(
  link: TraceLinkModel,
  onSuccess?: EmptyLambda
): Promise<void> {
  link.approvalStatus = ApprovalType.APPROVED;

  linkAPIHandler(link, updateApprovedLink, async () => {
    onSuccess?.();

    await projectModule.addOrUpdateTraceLinks([link]);
  });
}

/**
 * Processes link declines, setting the app state to loading in between, and updating trace links afterwards.
 *
 * @param link - The trace link to process.
 * @param onSuccess - Run when the API call successfully resolves.
 */
export async function handleDeclineLink(
  link: TraceLinkModel,
  onSuccess?: EmptyLambda
): Promise<void> {
  link.approvalStatus = ApprovalType.DECLINED;

  linkAPIHandler(link, updateDeclinedLink, async () => {
    onSuccess?.();

    await projectModule.deleteTraceLinks([link]);
  });
}

/**
 * Processes link API functions, setting the app state to loading in between.
 *
 * @param link - The trace link to process.
 * @param linkAPI - The endpoint to call with the link.
 * @param onSuccess - Run when the API call successfully resolves.
 */
function linkAPIHandler(
  link: TraceLinkModel,
  linkAPI: (traceLink: TraceLinkModel) => Promise<TraceLinkModel[]>,
  onSuccess: () => Promise<void>
): void {
  appModule.onLoadStart();
  linkAPI(link)
    .then(onSuccess)
    .finally(() => appModule.onLoadEnd());
}
