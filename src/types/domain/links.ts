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

/**
 * Link used when hiding subtrees to summarize the links of the children
 * of some root node.
 */
export interface SubtreeLink extends TraceLink {
  type: "SUBTREE";
  /**
   * The id of the artifact.
   */
  rootNode: string;
}

/**
 * The direction of trace links allowed by an artifact type.
 */
export interface ArtifactDirection {
  /**
   * The name of source the artifact type.
   */
  type: string;
  /**
   * The names of the allowed target types.
   */
  allowedTypes: string[];
}

/**
 * The direction of trace links allowed by an artifact type, with a label.
 */
export interface LabeledArtifactDirection extends ArtifactDirection {
  /**
   * The label to present an artifact direction.
   */
  label: string;
}
