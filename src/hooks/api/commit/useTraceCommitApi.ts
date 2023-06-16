import { defineStore } from "pinia";

import { ApprovalType, TraceLinkSchema } from "@/types";
import { commitApiStore } from "@/hooks";
import { pinia } from "@/plugins";

export const useTraceCommitApi = defineStore("traceCommitApi", () => {
  /**
   * Creates new trace links.
   *
   * @param traceLink - The trace link to persist.
   * @return The created trace links.
   */
  async function handleCreate(
    traceLink: TraceLinkSchema
  ): Promise<TraceLinkSchema[]> {
    traceLink = {
      ...traceLink,
      approvalStatus: ApprovalType.APPROVED,
    };

    return commitApiStore
      .handleSave((builder) => builder.withNewTraceLink(traceLink))
      .then((commit) => commit?.traces.added || []);
  }

  /**
   * Approves the given trace link ID.
   *
   * @param traceLink - The trace link to approve.
   * @return The modified trace links.
   */
  async function handleApprove(
    traceLink: TraceLinkSchema
  ): Promise<TraceLinkSchema[]> {
    traceLink = {
      ...traceLink,
      approvalStatus: ApprovalType.APPROVED,
    };

    return commitApiStore
      .handleSave((builder) => builder.withModifiedTraceLink(traceLink))
      .then((commit) => commit?.traces.modified || []);
  }

  /**
   * Declines the given trace link ID.
   *
   * @param traceLink - The trace link to decline.
   * @return The removed trace links.
   */
  async function handleDecline(
    traceLink: TraceLinkSchema
  ): Promise<TraceLinkSchema[]> {
    traceLink = {
      ...traceLink,
      approvalStatus: ApprovalType.DECLINED,
    };

    return commitApiStore
      .handleSave((builder) => builder.withModifiedTraceLink(traceLink))
      .then((commit) => commit?.traces.modified || []);
  }

  /**
   * Declines all given links.
   *
   * @param traceLinks - The trace links to decline.
   * @return The removed trace links.
   */
  async function handleDeclineAll(
    traceLinks: TraceLinkSchema[]
  ): Promise<TraceLinkSchema[]> {
    traceLinks = traceLinks.map((link) => ({
      ...link,
      approvalStatus: ApprovalType.DECLINED,
    }));

    return commitApiStore
      .handleSave((builder) => builder.withModifiedTraceLink(...traceLinks))
      .then((commit) => commit?.traces.modified || []);
  }

  /**
   * Declines the given trace link ID.
   *
   * @param traceLink - The trace link to decline.
   * @return The removed trace links.
   */
  async function handleUnreview(
    traceLink: TraceLinkSchema
  ): Promise<TraceLinkSchema[]> {
    traceLink = {
      ...traceLink,
      approvalStatus: ApprovalType.UNREVIEWED,
    };

    return commitApiStore
      .handleSave((builder) => builder.withModifiedTraceLink(traceLink))
      .then((commit) => commit?.traces.modified || []);
  }

  return {
    handleCreate,
    handleApprove,
    handleDecline,
    handleDeclineAll,
    handleUnreview,
  };
});

export default useTraceCommitApi(pinia);
