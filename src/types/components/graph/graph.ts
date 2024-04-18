import { ElementDefinition } from "cytoscape";
import { ClassNameProps, CytoCoreGraph, StyleProps } from "@/types";

/**
 * Enumerates the modes of the project graph.
 */
export type GraphMode = "tim" | "tree" | "table" | "delta" | "chat";

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
  graph: GraphMode;

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
 * The props for rendering a cytoscape element wrapper.
 */
export interface CyElementProps extends StyleProps {
  /**
   * The element to display.
   */
  definition: ElementDefinition;
}
