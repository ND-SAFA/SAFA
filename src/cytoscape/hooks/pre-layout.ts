import { EdgeSingular } from "cytoscape";
import { CytoCore, LayoutHook } from "@/types";
import {
  artifactHtml as nodeHTML,
  GENERATED_LINK_SELECTOR,
  GENERATED_TRACE_MAX_WIDTH,
} from "@/cytoscape/styles";

let nodeHtmlApplied = false;

/**
 * Applies HTML overlays to the graph nodes.
 *
 * @param cy - The cy instance.
 */
export const applyNodeHtml: LayoutHook = (cy: CytoCore): void => {
  if (nodeHtmlApplied) return;

  cy.nodeHtmlLabel([nodeHTML]);

  nodeHtmlApplied = true;
};

/**
 * Applies style changes to graph links.
 *
 * @param cy - The cy instance.
 */
export const applyOpacityToGeneratedLinks: LayoutHook = (
  cy: CytoCore
): void => {
  cy.edges(GENERATED_LINK_SELECTOR).forEach((edge: EdgeSingular) => {
    const score = edge.data().score;
    edge.style({
      width: score * GENERATED_TRACE_MAX_WIDTH,
    });
  });
};

/**
 * Validates and stores elements in layout objects applying custom styling as needed.
 */
export const DefaultPreLayoutHooks: LayoutHook[] = [
  applyNodeHtml,
  applyOpacityToGeneratedLinks,
];
