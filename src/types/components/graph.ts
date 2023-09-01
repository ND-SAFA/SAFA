import { ElementDefinition } from "cytoscape";
import {
  ArtifactDeltaState,
  ArtifactProps,
  ClassNameProps,
  CytoCoreGraph,
  StyleProps,
  ThemeColor,
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
 * The props for rendering a cytoscape graph.
 */
export interface CytoscapeProps extends ClassNameProps {
  /**
   * The id of this cytoscape graph.
   */
  id: string;
  /**
   * The graph configuration data.
   */
  graph: CytoCoreGraph;
}

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
 * The props for rendering a cytoscape element wrapper.
 */
export interface CyElementProps extends StyleProps {
  /**
   * The element to display.
   */
  definition: ElementDefinition;
}

/**
 * The props for rendering the display of a cytoscape node.
 */
export interface NodeDisplayProps {
  /**
   * The type of node to display.
   */
  variant: "tim" | "artifact" | "footer" | "sidebar" | "menu";
  /**
   * The color of the node to display.
   */
  color: ThemeColor;
  /**
   * The title of the node to display above the separator.
   */
  title?: string;
  /**
   * The subtitle of the node to display below the separator.
   */
  subtitle?: string;
  /**
   * Whether to display a separator between the title and subtitle.
   */
  separator?: boolean;
  /**
   * The body content to display.
   */
  body?: string;
  /**
   * Whether the node is selected.
   */
  selected?: boolean;
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
 * The props for rendering a trace link edge on the graph.
 */
export interface TraceLinkProps extends TraceProps {
  /**
   * The artifact ids currently selected in view.
   */
  artifactsInView: string[];
}

/**
 * The props for rendering an artifact type node on the graph.
 */
export interface TimNodeProps {
  /**
   * The artifact type to render.
   */
  artifactType: string;
  /**
   * The number of artifacts of this type.
   */
  count: number;
  /**
   * The icon to display for this artifact type.
   */
  icon?: string;
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
}
