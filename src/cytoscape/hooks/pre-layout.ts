import { CytoCore, LayoutHook } from "@/types";
import { EdgeSingular } from "cytoscape";
import {
  nodeHtml as nodeHTML,
  nodeWarningHtml,
} from "@/cytoscape/styles/html/node-html";
import { GENERATED_LINK_SELECTOR } from "@/cytoscape/styles/stylesheets/cytoscape";
import { GENERATED_TRACE_MAX_WIDTH } from "@/cytoscape/styles/config/trace";

export const applyNodeHtml: LayoutHook = (cy: CytoCore): void => {
  cy.nodeHtmlLabel([nodeHTML, nodeWarningHtml]);
};

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
