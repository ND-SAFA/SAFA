import {
  ArtifactModel,
  ArtifactData,
  ApprovalType,
  TraceLinkModel,
  TraceType,
  IOHandlerCallback,
} from "@/types";
import { appStore, logStore, traceStore, approvalStore } from "@/hooks";
import {
  createLink,
  updateApprovedLink,
  updateDeclinedLink,
  updateDeclinedLinks,
  updateUnreviewedLink,
} from "@/api";

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
    logStore.onSuccess(
      `Created a new trace link: ${sourceName} -> ${targetName}`
    );
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
 * @param onComplete - Called after the action.
 */
export async function handleApproveLink(
  link: TraceLinkModel,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  linkAPIHandler(link, updateApprovedLink, {
    onSuccess: (updatedLinks) => {
      traceStore.addOrUpdateTraceLinks(updatedLinks);
      approvalStore.approveLink(link);
      logStore.onSuccess(
        `Link has been approved: ${link.sourceName} -> ${link.targetName}`
      );
      onSuccess?.();
    },
    onError: (e) => {
      logStore.onError(
        `Unable to approve link: ${link.sourceName} -> ${link.targetName}`
      );
      onError?.(e);
    },
    onComplete,
  });
}

/**
 * Processes link declines, setting the app state to loading in between, and updating trace links afterwards.
 *
 * @param link - The trace link to process.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
export async function handleDeclineLink(
  link: TraceLinkModel,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  linkAPIHandler(link, updateDeclinedLink, {
    onSuccess: (updatedLinks) => {
      traceStore.deleteTraceLinks(updatedLinks);
      approvalStore.declineLink(link);
      logStore.onSuccess(
        `Link has been removed: ${link.sourceName} -> ${link.targetName}`
      );
      onSuccess?.();
    },
    onError: (e) => {
      logStore.onError(
        `Unable to decline link: ${link.sourceName} -> ${link.targetName}`
      );
      onError?.(e);
    },
    onComplete,
  });
}

/**
 * Declines all unreviewed links, setting the app state to loading in between, and updating trace links afterwards.
 */
export async function handleDeclineAll(): Promise<void> {
  logStore.confirm(
    "Clear Unreviewed Links",
    "Are you sure you want to remove all unreviewed links?",
    async (isConfirmed) => {
      if (!isConfirmed) return;

      const unreviewed = approvalStore.unreviewedLinks;

      try {
        appStore.onLoadStart();

        await updateDeclinedLinks(unreviewed);

        traceStore.deleteTraceLinks(unreviewed);
        unreviewed.map((link) => approvalStore.declineLink(link));

        logStore.onSuccess(`Removed unreviewed links: ${unreviewed.length}`);
      } catch (e) {
        unreviewed.map(
          (link) => (link.approvalStatus = ApprovalType.UNREVIEWED)
        );

        logStore.onError(`Unable to clear all links: ${unreviewed.length}`);
      } finally {
        appStore.onLoadEnd();
      }
    }
  );
}

/**
 * Processes link unreview, setting the app state to loading in between, and updating trace links afterwards.
 *
 * @param link - The trace link to process.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
export async function handleUnreviewLink(
  link: TraceLinkModel,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  linkAPIHandler(link, updateUnreviewedLink, {
    onSuccess: (updatedLinks) => {
      approvalStore.resetLink(link);
      traceStore.addOrUpdateTraceLinks(updatedLinks);
      logStore.onSuccess(
        `Link has been reset: ${link.sourceName} -> ${link.targetName}`
      );
      onSuccess?.();
    },
    onError: (e) => {
      logStore.onError(
        `Unable to reset link: ${link.sourceName} -> ${link.targetName}`
      );
      onError?.(e);
    },
    onComplete,
  });
}

/**
 * Deletes a trace link after confirmation.
 *
 * @param link - The trace link to delete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
export async function handleDeleteLink(
  link: TraceLinkModel,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  logStore.confirm(
    "Delete Trace Link",
    `Are you sure you want to delete "${link.sourceName} -> ${link.targetName}"?`,
    async (confirmed) => {
      if (!confirmed) return;

      await handleUnreviewLink(link, {
        onSuccess,
        onError,
        onComplete,
      });
    }
  );
}

/**
 * Processes link API functions, setting the app state to loading in between.
 *
 * @param link - The trace link to process.
 * @param linkAPI - The endpoint to call with the link.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */
function linkAPIHandler(
  link: TraceLinkModel,
  linkAPI: (traceLink: TraceLinkModel) => Promise<TraceLinkModel[]>,
  { onSuccess, onError, onComplete }: IOHandlerCallback<TraceLinkModel[]>
): void {
  appStore.onLoadStart();
  linkAPI(link)
    .then((updatedLinks) => onSuccess?.(updatedLinks))
    .catch((e) => onError?.(e))
    .finally(() => {
      appStore.onLoadEnd();
      onComplete?.();
    });
}
