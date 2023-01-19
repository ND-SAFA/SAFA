import { EdgeSingular } from "cytoscape";
import { CytoCore, LayoutHook } from "@/types";
import {
  artifactHtml,
  GENERATED_LINK_SELECTOR,
  GENERATED_TRACE_MAX_WIDTH,
  timNodeHtml,
} from "@/cytoscape/styles";

let ARTIFACT_LABEL_APPLIED = false;
let TIM_LABEL_APPLIED = false;

/**
 * Applies HTML overlays to the graph nodes.
 *
 * @param cy - The cy instance.
 */
export const applyTIMLabels: LayoutHook = (cy: CytoCore): void => {
  if (TIM_LABEL_APPLIED) return;

  cy.nodeHtmlLabel([timNodeHtml]);

  TIM_LABEL_APPLIED = true;
};

/**
 * Applies HTML overlays to the graph nodes.
 *
 * @param cy - The cy instance.
 */
export const applyArtifactLabels: LayoutHook = (cy: CytoCore): void => {
  if (ARTIFACT_LABEL_APPLIED) return;

  cy.nodeHtmlLabel([artifactHtml, timNodeHtml]);

  ARTIFACT_LABEL_APPLIED = true;
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
      width: Math.min(
        score * GENERATED_TRACE_MAX_WIDTH,
        GENERATED_TRACE_MAX_WIDTH
      ),
    });
  });
};

/**
 * Pre-layout hooks for the artifact tree.
 */
export const DefaultPreLayoutHooks: LayoutHook[] = [
  applyArtifactLabels,
  applyOpacityToGeneratedLinks,
];

/**
 * Pre-layout hooks for the TIM tree.
 */
export const TIMPreLayoutHooks: LayoutHook[] = [applyTIMLabels];
