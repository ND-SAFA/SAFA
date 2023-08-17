import {
  ArtifactDeltaState,
  ArtifactProps,
  TraceLinkSchema,
  TraceProps,
} from "@/types";

/**
 * Enumerates the modes of the project graph.
 */
export enum GraphMode {
  tim = "tim",
  tree = "tree",
  table = "table",
  delta = "delta",
}

/**
 * Enumerates the modes of the project graph.
 */
export enum GraphElementType {
  node = "node",
  edge = "edge",
}

/**
 * The required properties for defining an element (e.g. node or edge)
 * in cytoscape.
 */
export interface CytoElement<Data = CytoElementData> {
  /**
   * The data for the graph node or link.
   */
  data: Data;
  /**
   * The element's custom style.
   */
  style?: Record<string, unknown>;
  /**
   * The element's cytoscape classes.
   */
  classes?: string;
}

/**
 * Required properties for defining the data that is held within each
 * cytoscape element.
 */
export interface CytoElementData {
  /**
   * A unique identifier for the element with cytoscape instance.
   */
  id: string;
  /**
   * The type of element being represented.
   */
  type: GraphElementType;
  /**
   * The type of graph for this node.
   */
  graph: GraphMode.tree | GraphMode.tim;

  /**
   * Whether the app is running in dark mode.
   */
  dark: boolean;
  /**
   * The cytoscape label placed within nodes and besides edges.
   */
  label?: string;
}

/**
 * Required properties for defining a cytoscape edge.
 */
export interface CytoEdgeData extends CytoElementData {
  /**
   * The cytoscape element id to point from.
   */
  source: string;
  /**
   * The cytoscape element id to point toward.
   */
  target: string;
}

/**
 * Defines an artifact's data in cytoscape.
 */
export interface ArtifactCytoElementData extends CytoElementData {
  /**
   * The name of the artifact.
   */
  artifactName: string;
  /**
   * The type of the artifact.
   */
  artifactType: string;
}

/**
 * Defines an artifact element.
 */
export type ArtifactCytoElement = CytoElement<ArtifactCytoElementData>;

/**
 * Defines a trace link's data in cytoscape.
 */
export interface TraceCytoElementData
  extends CytoEdgeData,
    Pick<TraceLinkSchema, "traceType" | "approvalStatus"> {
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
 * Defines a tim node's data in cytoscape.
 */
export interface TimNodeCytoElementData extends CytoElementData {
  /**
   * The type of the artifact.
   */
  artifactType: string;
}

/**
 * Defines a tim node in cytoscape.
 */
export type TimNodeCytoElement = CytoElement<TimNodeCytoElementData>;

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
 * The props for rendering the TIM tree graph.
 */
export interface TimTreeProps {
  /**
   * Whether the tree is visible.
   */
  visible: boolean;
}

/**
 * The props for rendering an artifact node on the graph.
 */
export interface ArtifactNodeProps extends ArtifactProps {
  /**
   * The artifact ids currently selected in view.
   */
  artifactsInView: string[];
}

/**
 * The props for rendering artifact node display panels on the graph.
 */
export interface ArtifactNodeDisplayProps extends ArtifactProps {
  /**
   * The color of the artifact node.
   */
  color: string;
  /**
   * The color of the artifact node in delta state.
   */
  deltaColor: string;
  /**
   * Whether the artifact is selected.
   */
  selected: boolean;
  /**
   * The ids of the artifact's hidden children.
   */
  hiddenChildren: string[];
}

/**
 * The props for rendering a trace link on the graph.
 */
export interface TraceLinkProps extends TraceProps {
  /**
   * The artifact ids currently selected in view.
   */
  artifactsInView: string[];
}
