import {
  LayoutHook,
  AutoMoveReposition,
  CytoCore,
  IGraphLayout,
} from "@/types";
import { EventObject } from "cytoscape";
import { viewportModule } from "@/store";

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

export const centerViewOnRootNode: LayoutHook = (): void => {
  viewportModule.centerOnRootNode().then();
};

export const DefaultPostLayoutHooks: LayoutHook[] = [
  centerViewOnRootNode,
  applyAutoMoveEvents,
  applyCytoEvents,
];
