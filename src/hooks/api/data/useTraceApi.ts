import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  ArtifactSchema,
  ArtifactCytoElementData,
  TraceLinkSchema,
  IOHandlerCallback,
  TraceApiHook,
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

export const useTraceApi = defineStore("traceApi", (): TraceApiHook => {
  const createTraceApi = useApi("traceApi");
  const approveTraceApi = useApi("approveTraceApi");
  const unreviewTraceApi = useApi("unreviewTraceApi");
  const declineTraceApi = useApi("declineTraceApi");

  const createLoading = computed(() => createTraceApi.loading);
  const approveLoading = computed(() => approveTraceApi.loading);
  const unreviewLoading = computed(() => unreviewTraceApi.loading);
  const declineLoading = computed(() => declineTraceApi.loading);

  const loadingTraceIds = ref<string[]>([]);
  const loadTrace = (traceId: string) =>
    (loadingTraceIds.value = [...loadingTraceIds.value, traceId]);
  const unloadTrace = (traceId: string) =>
    (loadingTraceIds.value = loadingTraceIds.value.filter(
      (id) => id !== traceId
    ));

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
      traceType: "MANUAL",
      approvalStatus: "APPROVED",
      score: 1,
    };

    await createTraceApi.handleRequest(
      async () => {
        const createdLinks = await traceCommitApiStore.handleCreate(traceLink);

        traceStore.addOrUpdateTraceLinks(createdLinks);
        subtreeStore.addTraceSubtree(traceLink);
      },
      {
        ...callbacks,
        success: `Created a new trace link: ${sourceName} -> ${targetName}`,
        error: `Unable to create trace link: ${sourceName} -> ${targetName}`,
      }
    );
  }

  async function handleCreateAll(): Promise<void> {
    for (const target of traceSaveStore.targets) {
      for (const source of traceSaveStore.sources) {
        if (!source || !target) continue;

        await handleCreate(source, target);
      }
    }
  }

  async function handleApprove(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await approveTraceApi.handleRequest(
      async () => {
        loadTrace(traceLink.traceLinkId);

        const updatedLinks = await traceCommitApiStore.handleApprove(traceLink);

        traceStore.addOrUpdateTraceLinks(updatedLinks);
        approvalStore.approveLink(traceLink);
      },
      {
        ...callbacks,
        onComplete: () => {
          unloadTrace(traceLink.traceLinkId);
          callbacks.onComplete?.();
        },
        success: `Trace link approved: ${traceLink.sourceName} -> ${traceLink.targetName}`,
        error: `Unable to approve trace link: ${traceLink.sourceName} -> ${traceLink.targetName}`,
      }
    );
  }

  async function handleDecline(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await declineTraceApi.handleRequest(
      async () => {
        loadTrace(traceLink.traceLinkId);

        const updatedLinks = await traceCommitApiStore.handleDecline(traceLink);

        traceStore.deleteTraceLinks(updatedLinks);
        approvalStore.declineLink(traceLink);
        subtreeStore.deleteTraceSubtree(traceLink);
      },
      {
        ...callbacks,
        onComplete: () => {
          unloadTrace(traceLink.traceLinkId);
          callbacks.onComplete?.();
        },
        success: `Trace link declined: ${traceLink.sourceName} -> ${traceLink.targetName}`,
        error: `Unable to decline trace link: ${traceLink.sourceName} -> ${traceLink.targetName}`,
      }
    );
  }

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
              unreviewed.map((link) => (link.approvalStatus = "UNREVIEWED")),
            useAppLoad: true,
            success: `Removed unreviewed trace links: ${unreviewed.length}`,
            error: `Unable to clear unreviewed trace links: ${unreviewed.length}`,
          }
        );
      }
    );
  }

  async function handleUnreview(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await unreviewTraceApi.handleRequest(
      async () => {
        loadTrace(traceLink.traceLinkId);

        const updatedLinks = await traceCommitApiStore.handleUnreview(
          traceLink
        );

        traceStore.addOrUpdateTraceLinks(updatedLinks);
        approvalStore.resetLink(traceLink);
      },
      {
        ...callbacks,
        onComplete: () => {
          unloadTrace(traceLink.traceLinkId);
          callbacks.onComplete?.();
        },
        useAppLoad: true,
        success: `Trace link unreviewed: ${traceLink.sourceName} -> ${traceLink.targetName}`,
        error: `Unable to unreview trace link: ${traceLink.sourceName} -> ${traceLink.targetName}`,
      }
    );
  }

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
    loadingTraceIds,
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
