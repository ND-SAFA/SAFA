import { CytoElementData } from "@/types";

/**
 * Defines horizontal alignment options.
 */
type HorizontalAlignment = "center" | "left" | "right";

/**
 * Defines vertical alignment options.
 */
type VerticalAlignment = "center" | "top" | "bottom";

/**
 * Returns the html in string for the given artifact.
 */
type HtmlDefinitionFunction<T extends CytoElementData> = (data: T) => string;

/**
 * Defines an html node.
 */
export interface HtmlDefinition<T extends CytoElementData> {
  /**
   * The cytoscape query selector.
   * `cytoscape que./cytoscape-stylesheets`
   */
  query: string;
  /**
   * The title horizontal alignment.
   */
  halign: HorizontalAlignment;
  /**
   * The title vertical alignment.
   */
  valign: VerticalAlignment;
  /**
   * The horizontal alignment of the box.
   */
  halignBox: HorizontalAlignment;
  /**
   * The vertical alignment of the box.
   */
  valignBox: VerticalAlignment;
  /**
   * Returns the stringified html of a given artifact.
   */
  tpl: HtmlDefinitionFunction<T>;
}

/**
 * Represents position styling for an SVG.
 */
export interface SvgStyle {
  /**
   * The x position to draw at.
   */
  x: number;
  /**
   * The y position to draw at.
   */
  y: number;
  /**
   * The width to draw.
   */
  width: number;
  /**
   * The height to draw.
   */
  height: number;
  /**
   * The color to render.
   */
  color?: string;
  /**
   * The class names to append.
   */
  class?: string;
}

/**
 * Represents position styling for an SVG.
 */
export interface SvgNodeStyle {
  /**
   * The outer dimensions of the node.
   */
  outer: Pick<SvgStyle, "width" | "height">;
  /**
   * THe style of the inner content of the node.
   */
  inner: SvgStyle;
  /**
   * The top margin to to add to the node.
   */
  marginTop: number;
  /**
   * The maximum amount of body characters to render.
   */
  truncateLength: number;
  /**
   * The width of the node's body, if it is different than the inner style.
   */
  bodyWidth?: number;
}

/**
 * Represents a type of child delta to render on a parent artifact.
 */
export interface NodeChildDelta {
  /**
   * The color of delta to render.
   */
  color: string;
}
