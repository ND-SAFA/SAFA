import { EdgeSingular } from "cytoscape";
import { CytoCore, LayoutHook } from "@/types";
import {
  GENERATED_LINK_SELECTOR,
  GENERATED_TRACE_MAX_WIDTH,
} from "@/cytoscape/styles";

/**
 * Applies style changes to graph links.
 *
 * @param cy - The cy instance.
 */
export const styleGeneratedLinks: LayoutHook = (cy: CytoCore): void => {
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
export const DefaultPreLayoutHooks: LayoutHook[] = [styleGeneratedLinks];

/**
 * Pre-layout hooks for the TIM tree.
 */
export const CreatorPreLayoutHooks: LayoutHook[] = [];
