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
export interface CytoCoreElementDefinition<Data = CytoCoreElementData> {
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
export interface CytoCoreElementData {
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
   * The cytoscape label placed within nodes and besides edges.
   */
  label?: string;
}

/**
 * Defines an artifact's data in cytoscape.
 */
export interface ArtifactData extends CytoCoreElementData {
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

  /**
   * Whether the app is running in dark mode.
   */
  dark: boolean;
}

/**
 * Defines an artifact element.
 */
export interface ArtifactCytoCoreElement
  extends CytoCoreElementDefinition<ArtifactData> {
  /**
   * The artifact's position in the graph
   */
  position?: PositionSchema;
}

/**
 * Defines a trace link's data in cytoscape.
 */
export interface TraceData
  extends CytoCoreElementData,
    Pick<TraceLinkSchema, "traceType" | "approvalStatus"> {
  /**
   * The cytoscape element id to point from.
   */
  source: string;
  /**
   * The cytoscape element id to point toward.
   */
  target: string;
  /**
   * The state of changes to the trace link.
   */
  deltaType: ArtifactDeltaState;
  /**
   * The count to display on the trace link.
   */
  count?: number;
  /**
   * Whether to fade this trace link.
   */
  faded?: boolean;
}

/**
 * Defines a trace link element.
 */
export type TraceCytoCoreElement = CytoCoreElementDefinition<TraceData>;

/**
 * Defines a tim node's data in cytoscape.
 */
export interface TimNodeData extends CytoCoreElementData {
  /**
   * The number of artifacts of this artifact type.
   */
  count: number;
}

/**
 * Defines a tim node in cytoscape.
 */
export type TimNodeDefinition = CytoCoreElementDefinition<TimNodeData>;

/**
 * Defines a tim edge's data in cytoscape.
 */
export interface TimEdgeData extends CytoCoreElementData {
  /**
   * The number of links between these artifact layers.
   */
  count: number;
  /**
   * The artifact type that this matrix goes from.
   */
  sourceType: string;
  /**
   * The artifact type that this matrix goes to.
   */
  targetType: string;
}

/**
 * Defines a tim edge in cytoscape.
 */
export type TimEdgeDefinition = CytoCoreElementDefinition<TimEdgeData>;
