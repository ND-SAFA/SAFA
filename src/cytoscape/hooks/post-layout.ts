import { LayoutHook } from "@/types/cytoscape/klay";
import { AutoMoveReposition } from "@/types/cytoscape/automove";
import { CytoCore } from "@/types/cytoscape";
import IGraphLayout from "@/types/cytoscape/igraph-layout";
import { EventObject } from "cytoscape";
import {
  ANIMATION_DURATION,
  CENTER_GRAPH_PADDING,
} from "@/cytoscape/styles/config/graph";

export const applyAutoMoveEvents: LayoutHook = (
  cy: CytoCore,
  layout: IGraphLayout
): void => {
  cy.nodes().forEach((node) => {
    const rule = cy.automove({
      nodesMatching: node.successors("node"),
      reposition: AutoMoveReposition.DRAG,
      dragWith: node,
    });
    for (const eventDefinition of Object.values(layout.autoMoveHandlers)) {
      node.on(eventDefinition.triggers.join(" "), (event: EventObject) => {
        eventDefinition.action(node, rule, event);
      });
    }
  });
};

export const applyCytoEvents: LayoutHook = (
  cy: CytoCore,
  layout: IGraphLayout
): void => {
  for (const cytoEvent of Object.values(layout.cytoEventHandlers)) {
    const eventName: string = cytoEvent.events.join(" ");
    const selector = cytoEvent.selector;
    const handler = (event: EventObject) => cytoEvent.action(cy, event);
    if (selector === undefined) {
      cy.on(eventName, handler);
    } else {
      cy.on(eventName, selector, handler);
    }
  }
};

export const centerView: LayoutHook = (cy: CytoCore): void => {
  cy.animate({
    fit: { eles: cy.nodes(), padding: CENTER_GRAPH_PADDING },
    duration: ANIMATION_DURATION,
  });
};

export const DefaultPostLayoutHooks: LayoutHook[] = [
  centerView,
  applyAutoMoveEvents,
  applyCytoEvents,
];
