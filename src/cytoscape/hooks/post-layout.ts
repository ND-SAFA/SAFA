import { EventObject, NodeSingular } from "cytoscape";
import {
  LayoutHook,
  AutoMoveReposition,
  CytoCore,
  IGraphLayout,
} from "@/types";
import { artifactSelectionModule, viewportModule } from "@/store";

/**
 * Adds automove handlers to a node, so that its child nodes are dragged along with it.
 *
 * @param cy - The Cytocore instance.
 * @param layout - The layout instance.
 * @param node - The node to add handlers for.
 */
export function addAutoMoveToNode(
  cy: CytoCore,
  layout: IGraphLayout,
  node: NodeSingular
): void {
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
}

export const applyAutoMoveEvents: LayoutHook = (
  cy: CytoCore,
  layout: IGraphLayout
): void => {
  cy.automove("destroy");
  cy.nodes().forEach((node) => addAutoMoveToNode(cy, layout, node));
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
  const selectedArtifacts = artifactSelectionModule.getSelectedArtifactId;

  if (!selectedArtifacts) {
    viewportModule.centerOnRootNode().then();
  } else {
    viewportModule.centerOnArtifacts([selectedArtifacts]).then();
  }
};

export const DefaultPostLayoutHooks: LayoutHook[] = [
  centerViewOnRootNode,
  applyAutoMoveEvents,
  applyCytoEvents,
];
