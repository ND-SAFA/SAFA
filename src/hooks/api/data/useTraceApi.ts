import { defineStore } from "pinia";

import {
  ArtifactSchema,
  ArtifactCytoElementData,
  ApprovalType,
  TraceLinkSchema,
  TraceType,
  IOHandlerCallback,
} from "@/types";
import { useApi, logStore, traceStore, approvalStore } from "@/hooks";
import {
  createLink,
  updateApprovedLink,
  updateDeclinedLink,
  updateDeclinedLinks,
  updateUnreviewedLink,
} from "@/api";
import { pinia } from "@/plugins";

export const useTraceApi = defineStore("traceApi", () => {
  const traceApi = useApi("traceApi");

  /**
   * Creates a new trace link.
   *
   * @param source - The artifact to link from.
   * @param target - The artifact to link to.
   */
  async function handleCreate(
    source: ArtifactSchema | ArtifactCytoElementData,
    target: ArtifactSchema | ArtifactCytoElementData
  ): Promise<void> {
    const sourceName =
      "artifactName" in source ? source.artifactName : source.name;
    const targetName =
      "artifactName" in target ? target.artifactName : target.name;

    const traceLink: TraceLinkSchema = {
      traceLinkId: "",
      sourceId: source.id,
      sourceName,
      targetId: target.id,
      targetName,
      traceType: TraceType.MANUAL,
      approvalStatus: ApprovalType.APPROVED,
      score: 1,
    };

    await traceApi.handleRequest(
      async () => {
        const createdLinks = await createLink(traceLink);

        traceStore.addOrUpdateTraceLinks(createdLinks);
      },
      {},
      {
        success: `Created a new trace link: ${sourceName} -> ${targetName}`,
        error: `Unable to create trace link: ${sourceName} -> ${targetName}`,
      }
    );
  }

  /**
   * Processes link approvals, setting the app state to loading in between, and updating trace links afterwards.
   *
   * @param traceLink - The trace link to process.
   * @param callbacks - The callbacks to call after the action.
   */
  async function handleApprove(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await traceApi.handleRequest(
      async () => {
        const updatedLinks = await updateApprovedLink(traceLink);

        traceStore.addOrUpdateTraceLinks(updatedLinks);
        approvalStore.approveLink(traceLink);
      },
      callbacks,
      {
        success: `Trace link approved: ${traceLink.sourceName} -> ${traceLink.targetName}`,
        error: `Unable to approve trace link: ${traceLink.sourceName} -> ${traceLink.targetName}`,
      }
    );
  }

  /**
   * Processes link declines, setting the app state to loading in between, and updating trace links afterwards.
   *
   * @param traceLink - The trace link to process.
   * @param callbacks - The callbacks to call after the action.
   */
  async function handleDecline(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await traceApi.handleRequest(
      async () => {
        const updatedLinks = await updateDeclinedLink(traceLink);

        await traceStore.deleteTraceLinks(updatedLinks);
        approvalStore.declineLink(traceLink);
      },
      callbacks,
      {
        success: `Trace link declined: ${traceLink.sourceName} -> ${traceLink.targetName}`,
        error: `Unable to decline trace link: ${traceLink.sourceName} -> ${traceLink.targetName}`,
      }
    );
  }

  /**
   * Declines all unreviewed links, setting the app state to loading in between, and updating trace links.
   */
  async function handleDeclineAll(): Promise<void> {
    await logStore.confirm(
      "Clear Unreviewed Links",
      "Are you sure you want to remove all unreviewed links?",
      async (isConfirmed) => {
        if (!isConfirmed) return;

        const unreviewed = approvalStore.unreviewedLinks;

        await traceApi.handleRequest(
          async () => {
            await updateDeclinedLinks(unreviewed);

            await traceStore.deleteTraceLinks(unreviewed);
            unreviewed.map((link) => approvalStore.declineLink(link));
          },
          {
            onError: () =>
              unreviewed.map(
                (link) => (link.approvalStatus = ApprovalType.UNREVIEWED)
              ),
          },
          {
            useAppLoad: true,
            success: `Removed unreviewed trace links: ${unreviewed.length}`,
            error: `Unable to clear unreviewed trace links: ${unreviewed.length}`,
          }
        );
      }
    );
  }

  /**
   * Processes link unreview, setting the app state to loading in between, and updating trace links afterwards.
   *
   * @param traceLink - The trace link to process.
   * @param callbacks - The callbacks to call after the action.
   */
  async function handleUnreview(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await traceApi.handleRequest(
      async () => {
        const updatedLinks = await updateUnreviewedLink(traceLink);

        traceStore.addOrUpdateTraceLinks(updatedLinks);
        approvalStore.resetLink(traceLink);
      },
      callbacks,
      {
        useAppLoad: true,
        success: `Trace link unreviewed: ${traceLink.sourceName} -> ${traceLink.targetName}`,
        error: `Unable to unreview trace link: ${traceLink.sourceName} -> ${traceLink.targetName}`,
      }
    );
  }

  /**
   * Deletes a trace link after confirmation.
   *
   * @param traceLink - The trace link to delete.
   * @param callbacks - The callbacks to call after the action.
   */
  async function handleDelete(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    logStore.confirm(
      "Delete Trace Link",
      `Are you sure you want to delete "${traceLink.sourceName} -> ${traceLink.targetName}"?`,
      async (confirmed) => {
        if (!confirmed) return;

        await handleDecline(traceLink, callbacks);
      }
    );
  }

  return {
    handleCreate,
    handleApprove,
    handleDecline,
    handleDeclineAll,
    handleUnreview,
    handleDelete,
  };
});

export default useTraceApi(pinia);
