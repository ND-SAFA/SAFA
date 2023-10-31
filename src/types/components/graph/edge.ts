import {
  ArtifactDeltaState,
  CytoEdgeData,
  CytoElement,
  TraceLinkSchema,
  TraceProps,
} from "@/types";

/**
 * Defines a trace link's data in cytoscape.
 */
export interface TraceCytoElementData
  extends CytoEdgeData,
    Pick<TraceLinkSchema, "traceType" | "approvalStatus" | "score"> {
  /**
   * The state of changes to the trace link.
   */
  deltaType?: ArtifactDeltaState;
  /**
   * Whether to fade this trace link.
   */
  faded?: boolean;
}

/**
 * Defines a trace link element.
 */
export type TraceCytoElement = CytoElement<TraceCytoElementData>;

/**
 * Defines a tim edge's data in cytoscape.
 */
export interface TimEdgeCytoElementData extends CytoEdgeData {
  /**
   * The name of the source artifact type.
   */
  sourceType: string;
  /**
   The name of the target artifact type.
   */
  targetType: string;
  /**
   * The number of links between these artifact layers.
   */
  count: number;
  /**
   * Whether this edge contains generated links.
   */
  generated: boolean;
}

/**
 * Defines a tim edge in cytoscape.
 */
export type TimEdgeCytoElement = CytoElement<TimEdgeCytoElementData>;

/**
 * The props for rendering a trace link edge on the graph.
 */
export interface TraceLinkProps extends TraceProps {
  /**
   * The artifact ids currently selected in view.
   */
  artifactsInView: string[];
}

/**
 * The props for rendering a trace matrix edge on the graph.
 */
export interface TimLinkProps {
  /**
   * The source artifact type to render.
   */
  sourceType: string;
  /**
   * The target artifact type to render.
   */
  targetType: string;
  /**
   * The number of trace links of this type.
   */
  count: number;
  /**
   * Whether this matrix contains generated links.
   */
  generated?: boolean;
  /**
   * If true, the actions for this edge will be hidden.
   */
  hideActions?: boolean;
}
