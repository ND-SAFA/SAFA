/**
 * Enumerates the type of trace approvals.
 */
export enum ApprovalType {
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
 * Enumerates the type of traces used internally.
 */
export enum InternalTraceType {
  SUBTREE = "SUBTREE",
}

/**
 * Defines a link.
 */
export interface LinkModel {
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
export interface TraceLinkModel extends LinkModel {
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
}

/**
 * Represents a trace link merged with other properties.
 */
export interface FlatTraceLink extends TraceLinkModel {
  /**
   * The type of source artifact.
   */
  sourceType: string;
  /**
   * The type of target artifact.
   */
  targetType: string;
}

/**
 * Link used when hiding subtrees to summarize the links of the children
 * of some root node.
 */
export interface SubtreeLinkModel extends TraceLinkModel {
  type: InternalTraceType.SUBTREE;
  /**
   * The id of the artifact.
   */
  rootNode: string;
}

/**
 * The direction of trace links allowed by an artifact type.
 */
export interface TraceDirectionModel {
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
export interface LabelledTraceDirectionModel extends TraceDirectionModel {
  /**
   * The label to present an artifact direction.
   */
  label: string;
  /**
   * The icon representing this artifact type.
   */
  icon: string;
  /**
   * The index of the icon representing this artifact type.
   */
  iconIndex: number;
}
