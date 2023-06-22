import { defineStore } from "pinia";

import { computed } from "vue";
import {
  ArtifactSchema,
  ArtifactCytoElementData,
  ApprovalType,
  TraceLinkSchema,
  TraceType,
  IOHandlerCallback,
} from "@/types";
import {
  useApi,
  logStore,
  traceStore,
  approvalStore,
  traceCommitApiStore,
  subtreeStore,
  traceSaveStore,
} from "@/hooks";
import { pinia } from "@/plugins";

export const useTraceApi = defineStore("traceApi", () => {
  const createTraceApi = useApi("traceApi");
  const approveTraceApi = useApi("approveTraceApi");
  const unreviewTraceApi = useApi("unreviewTraceApi");
  const declineTraceApi = useApi("declineTraceApi");

  const createLoading = computed(() => createTraceApi.loading);
  const approveLoading = computed(() => approveTraceApi.loading);
  const unreviewLoading = computed(() => unreviewTraceApi.loading);
  const declineLoading = computed(() => declineTraceApi.loading);

  /**
   * Creates a new trace link.
   *
   * @param source - The artifact to link from.
   * @param target - The artifact to link to.
   * @param callbacks - The callbacks to call after the action.
   */
  async function handleCreate(
    source: ArtifactSchema | ArtifactCytoElementData,
    target: ArtifactSchema | ArtifactCytoElementData,
    callbacks: IOHandlerCallback = {}
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

    await createTraceApi.handleRequest(
      async () => {
        const createdLinks = await traceCommitApiStore.handleCreate(traceLink);

        traceStore.addOrUpdateTraceLinks(createdLinks);
        subtreeStore.addTraceSubtree(traceLink);
      },
      callbacks,
      {
        success: `Created a new trace link: ${sourceName} -> ${targetName}`,
        error: `Unable to create trace link: ${sourceName} -> ${targetName}`,
      }
    );
  }

  /**
   * Creates a new trace link between all source to all target artifacts in the saved trace store.
   */
  async function handleCreateAll(): Promise<void> {
    for (const target of traceSaveStore.targets) {
      for (const source of traceSaveStore.sources) {
        if (!source || !target) continue;

        await handleCreate(source, target);
      }
    }
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
    await approveTraceApi.handleRequest(
      async () => {
        const updatedLinks = await traceCommitApiStore.handleApprove(traceLink);

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
    await declineTraceApi.handleRequest(
      async () => {
        const updatedLinks = await traceCommitApiStore.handleDecline(traceLink);

        traceStore.deleteTraceLinks(updatedLinks);
        approvalStore.declineLink(traceLink);
        subtreeStore.deleteTraceSubtree(traceLink);
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

        await declineTraceApi.handleRequest(
          async () => {
            await traceCommitApiStore.handleDeclineAll(unreviewed);

            traceStore.deleteTraceLinks(unreviewed);
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
    await unreviewTraceApi.handleRequest(
      async () => {
        const updatedLinks = await traceCommitApiStore.handleUnreview(
          traceLink
        );

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
    createLoading,
    approveLoading,
    declineLoading,
    unreviewLoading,
    handleCreate,
    handleCreateAll,
    handleApprove,
    handleDecline,
    handleDeclineAll,
    handleUnreview,
    handleDelete,
  };
});

export default useTraceApi(pinia);
