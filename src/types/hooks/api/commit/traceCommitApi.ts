import { TraceLinkSchema } from "@/types";

/**
 * A hook for calling trace commit API endpoints.
 */
export interface TraceCommitApiHook {
  /**
   * Creates new trace links.
   *
   * @param traceLink - The trace link to persist.
   * @param preserveApproval - Whether to preserve the approval status.
   *        @default to false.
   * @return The created trace links.
   */
  handleCreate(
    traceLink: TraceLinkSchema,
    preserveApproval?: boolean
  ): Promise<TraceLinkSchema[]>;
  /**
   * Approves the given trace link ID.
   *
   * @param traceLink - The trace link to approve.
   * @return The modified trace links.
   */
  handleApprove(traceLink: TraceLinkSchema): Promise<TraceLinkSchema[]>;
  /**
   * Declines the given trace link ID.
   *
   * @param traceLink - The trace link to decline.
   * @return The removed trace links.
   */
  handleDecline(traceLink: TraceLinkSchema): Promise<TraceLinkSchema[]>;
  /**
   * Declines all given links.
   *
   * @param traceLinks - The trace links to decline.
   * @return The removed trace links.
   */
  handleDeclineAll(traceLinks: TraceLinkSchema[]): Promise<TraceLinkSchema[]>;
  /**
   * Declines the given trace link ID.
   *
   * @param traceLink - The trace link to decline.
   * @return The removed trace links.
   */
  handleUnreview(traceLink: TraceLinkSchema): Promise<TraceLinkSchema[]>;
}
