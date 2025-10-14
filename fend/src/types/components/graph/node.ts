import {
  ArtifactProps,
  CytoElement,
  CytoElementData,
  ThemeColor,
} from "@/types";

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
  /**
   * If true, the actions for this node will be hidden.
   */
  hideActions?: boolean;
}
