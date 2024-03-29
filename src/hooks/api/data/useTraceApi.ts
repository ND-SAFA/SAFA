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
  const editTraceApi = useApi("editTraceApi");

  const approveTraceApi = useApi("approveTraceApi");
  const unreviewTraceApi = useApi("unreviewTraceApi");
  const declineTraceApi = useApi("declineTraceApi");

  const createLoading = computed(() => createTraceApi.loading);
  const editLoading = computed(() => editTraceApi.loading);
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
    explanation = "",
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    const sourceName =
      "artifactName" in source ? source.artifactName : source.name;
    const targetName =
      "artifactName" in target ? target.artifactName : target.name;
    const traceName = `${sourceName} -> ${targetName}`;

    const traceLink: TraceLinkSchema = {
      traceLinkId: "",
      sourceId: source.id,
      sourceName,
      targetId: target.id,
      targetName,
      traceType: "MANUAL",
      approvalStatus: "APPROVED",
      score: 1,
      explanation,
    };

    await createTraceApi.handleRequest(
      async () => {
        const createdLinks = await traceCommitApiStore.handleCreate(traceLink);

        traceStore.addOrUpdateTraceLinks(createdLinks);
        subtreeStore.addTraceSubtree(traceLink);
      },
      {
        ...callbacks,
        success: `Created a new trace link: ${traceName}`,
        error: `Unable to create trace link: ${traceName}`,
      }
    );
  }

  async function handleCreateAll(): Promise<void> {
    for (const target of traceSaveStore.targets) {
      for (const source of traceSaveStore.sources) {
        if (!source || !target) continue;

        await handleCreate(source, target, traceSaveStore.explanation);
      }
    }
  }

  async function handleApprove(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    const traceName = `${traceLink.sourceName} -> ${traceLink.targetName}`;

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
        success: `Trace link approved: ${traceName}`,
        error: `Unable to approve trace link: ${traceName}`,
      }
    );
  }

  async function handleDecline(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    const traceName = `${traceLink.sourceName} -> ${traceLink.targetName}`;

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
        success: `Trace link declined: ${traceName}`,
        error: `Unable to decline trace link: ${traceName}`,
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
    const traceName = `${traceLink.sourceName} -> ${traceLink.targetName}`;

    await unreviewTraceApi.handleRequest(
      async () => {
        loadTrace(traceLink.traceLinkId);

        const updatedLinks =
          await traceCommitApiStore.handleUnreview(traceLink);

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
        success: `Trace link unreviewed: ${traceName}`,
        error: `Unable to unreview trace link: ${traceName}`,
      }
    );
  }

  async function handleEdit(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    const traceName = `${traceLink.sourceName} -> ${traceLink.targetName}`;

    await editTraceApi.handleRequest(
      async () => {
        const editedLinks = await traceCommitApiStore.handleCreate(
          traceLink,
          true
        );

        traceStore.addOrUpdateTraceLinks(editedLinks);
      },
      {
        ...callbacks,
        success: `Edited trace link: ${traceName}`,
        error: `Unable to edit trace link: ${traceName}`,
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
    editLoading,
    approveLoading,
    declineLoading,
    unreviewLoading,
    handleCreate,
    handleCreateAll,
    handleApprove,
    handleDecline,
    handleDeclineAll,
    handleUnreview,
    handleEdit,
    handleDelete,
  };
});

export default useTraceApi(pinia);
