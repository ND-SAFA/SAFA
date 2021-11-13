import { ArtifactData } from "@/types/domain";

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
type HtmlDefinitionFunction = (data: ArtifactData) => string;

/**
 * Defines an html node.
 */
export interface HtmlDefinition {
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
  tpl: HtmlDefinitionFunction;
}
