import {
  ArtifactDeltaState,
  WarningSchema,
  FTANodeType,
  PositionSchema,
  SafetyCaseType,
  TraceLinkSchema,
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
  classes?: string[];
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
   * The id of the artifact.
   */
  id: string;
  /**
   * The content of the artifact.
   */
  body: string;
  /**
   * Any warnings generated from the artifact.
   */
  warnings?: WarningSchema[];
  /**
   * The name of the artifact.
   */
  artifactName: string;
  /**
   * The type of the artifact.
   */
  artifactType: string;
  /**
   * For FTA nodes, the logic type of the artifact.
   */
  logicType?: FTANodeType;
  /**
   * For safety case nodes, the type of the artifact.
   */
  safetyCaseType?: SafetyCaseType;
  /**
   * The state of changes to the artifact.
   */
  artifactDeltaState: ArtifactDeltaState;
  /**
   * Whether the artifact is selected.
   */
  isSelected: boolean;
  /**
   * The opacity of this artifact.
   */
  opacity: number;

  /**
   * The number of hidden child elements.
   */
  hiddenChildren?: number;
  /**
   * The delta states of any hidden children.
   */
  childDeltaStates?: ArtifactDeltaState[];
  /**
   * Any warnings in child elements.
   */
  childWarnings?: WarningSchema[];
}

/**
 * Defines an artifact element.
 */
export interface ArtifactCytoElement
  extends CytoElement<ArtifactCytoElementData> {
  /**
   * The artifact's position in the graph
   */
  position?: PositionSchema;
}

/**
 * Defines a trace link's data in cytoscape.
 */
export interface TraceCytoElementData
  extends CytoEdgeData,
    Pick<TraceLinkSchema, "traceType" | "approvalStatus"> {
  /**
   * The state of changes to the trace link.
   */
  deltaType: ArtifactDeltaState;
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
  /**
   * The number of artifacts of this artifact type.
   */
  count: number;
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
