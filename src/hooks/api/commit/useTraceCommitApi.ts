import { defineStore } from "pinia";

import { TraceLinkSchema, TraceCommitApiHook } from "@/types";
import { commitApiStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * A hook for managing trace commit API requests.
 */
export const useTraceCommitApi = defineStore(
  "traceCommitApi",
  (): TraceCommitApiHook => {
    async function handleCreate(
      traceLink: TraceLinkSchema,
      preserveApproval = false
    ): Promise<TraceLinkSchema[]> {
      traceLink = {
        ...traceLink,
        ...(preserveApproval ? {} : { approvalStatus: "APPROVED" }),
      };

      return commitApiStore
        .handleSave((builder) => builder.withNewTraceLink(traceLink))
        .then((commit) => commit?.traces.added || []);
    }

    async function handleApprove(
      traceLink: TraceLinkSchema
    ): Promise<TraceLinkSchema[]> {
      traceLink = {
        ...traceLink,
        approvalStatus: "APPROVED",
      };

      return commitApiStore
        .handleSave((builder) => builder.withModifiedTraceLink(traceLink))
        .then((commit) => commit?.traces.modified || []);
    }

    async function handleDecline(
      traceLink: TraceLinkSchema
    ): Promise<TraceLinkSchema[]> {
      traceLink = {
        ...traceLink,
        approvalStatus: "DECLINED",
      };

      return commitApiStore
        .handleSave((builder) => builder.withModifiedTraceLink(traceLink))
        .then((commit) => commit?.traces.modified || []);
    }

    async function handleDeclineAll(
      traceLinks: TraceLinkSchema[]
    ): Promise<TraceLinkSchema[]> {
      traceLinks = traceLinks.map((link) => ({
        ...link,
        approvalStatus: "DECLINED",
      }));

      return commitApiStore
        .handleSave((builder) => builder.withModifiedTraceLink(...traceLinks))
        .then((commit) => commit?.traces.modified || []);
    }

    async function handleUnreview(
      traceLink: TraceLinkSchema
    ): Promise<TraceLinkSchema[]> {
      traceLink = {
        ...traceLink,
        approvalStatus: "UNREVIEWED",
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
  }
);

export default useTraceCommitApi(pinia);
