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
 * Enumerates the type of generated trace models.
 */
export enum ModelType {
  AutomotiveBert = "AutomotiveBert",
  NLBert = "NLBert",
  PLBert = "PLBert",
  VSM = "VSM",
}

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
 * Link used when hiding subtrees to summarize the links of the children
 * of some root node.
 */
export interface SubtreeLinkSchema extends TraceLinkSchema {
  type: InternalTraceType.SUBTREE;
  /**
   * The id of the artifact.
   */
  rootNode: string;
}

/**
 * The direction of trace links allowed by an artifact type.
 */
export interface TraceDirectionSchema {
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
export interface LabelledTraceDirectionSchema extends TraceDirectionSchema {
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
