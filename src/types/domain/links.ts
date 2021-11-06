/**
 * Enumerates the type of trace approvals.
 */
export enum TraceApproval {
  UNREVIEWED = "UNREVIEWED",
  APPROVED = "APPROVED",
  DECLINED = "DECLINED",
}

/**
 * Enumerates the type of traces.
 */
export enum TraceType {
  GENERATED = "GENERATED",
  MANUAL = "MANUAL",
}

/**
 * Defines a link.
 */
export interface Link {
  /**
   * The source node ID.
   */
  source: string;
  /**
   * The target node ID.
   */
  target: string;
}

/**
 * Defines a trace link.
 */
export interface TraceLink extends Link {
  /**
   * The trace link ID.
   */
  traceLinkId: string;
  /**
   * The approval status of the trace.
   */
  approvalStatus: TraceApproval;
  /**
   * The confidence score of the trace.
   */
  score: number;
  /**
   * The type of trace.
   */
  traceType: TraceType;
}

/**
 * Defines a displayable trace link.
 */
export interface TraceLinkDisplayData extends TraceLink {
  /**
   * The body of the source of the link.
   */
  sourceBody: string;
  /**
   * The body of the target of the link.
   */
  targetBody: string;
}
