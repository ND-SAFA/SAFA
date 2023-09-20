/**
 * Enumerates the type of trace approvals.
 */
export type ApprovalType = "UNREVIEWED" | "APPROVED" | "DECLINED";

/**
 * Enumerates the type of traces.
 */
export type TraceType = "GENERATED" | "MANUAL";

/**
 * Defines a link.
 */
export interface LinkSchema {
  /**
   * The source node ID.
   */
  sourceId: string;
  /**
   * The source node name.
   */
  sourceName: string;
  /**
   * The target node ID.
   */
  targetId: string;
  /**
   * The target node name.
   */
  targetName: string;
}

/**
 * Defines a trace link.
 */
export interface TraceLinkSchema extends LinkSchema {
  /**
   * The trace link ID.
   */
  traceLinkId: string;
  /**
   * The approval status of the trace.
   */
  approvalStatus: ApprovalType;
  /**
   * The confidence score of the trace.
   */
  score: number;
  /**
   * The type of trace.
   */
  traceType: TraceType;
  /**
   * The explanation of why a trace link was generated.
   */
  explanation?: string;
}

/**
 * Represents a trace link merged with other properties.
 */
export interface FlatTraceLink extends TraceLinkSchema {
  /**
   * The type of source artifact.
   */
  sourceType: string;
  /**
   * The body of source artifact.
   */
  sourceBody: string;
  /**
   * The type of target artifact.
   */
  targetType: string;
  /**
   * The body of target artifact.
   */
  targetBody: string;
}

/**
 * Represents links generated for a project.
 */
export interface GeneratedLinksSchema {
  /**
   * All generated links.
   */
  traceLinks: FlatTraceLink[];
  /**
   * Approved generated link ids.
   */
  approvedIds: string[];
  /**
   * Declined generated link ids.
   */
  declinedIds: string[];
}
