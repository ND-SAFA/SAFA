import { EventObject, NodeSingular } from "cytoscape";
import { LayoutHook, AutoMoveReposition, CytoCore, CyLayout } from "@/types";
import { cyStore, selectionStore } from "@/hooks";

/**
 * Adds auto-move handlers to a node, so that its child nodes are dragged along with it.
 *
 * @param cy - The cy instance.
 * @param layout - The layout instance.
 * @param node - The node to add handlers for.
 */
export function addAutoMoveToNode(
  cy: CytoCore,
  layout: CyLayout,
  node: NodeSingular
): void {
  const children = node
    .connectedEdges(`edge[source='${node.data().id}']`)
    .targets();

  const rule = cy.automove({
    nodesMatching: children.union(children.successors()),
    reposition: AutoMoveReposition.DRAG,
    dragWith: node,
  });

  for (const eventDefinition of Object.values(layout.autoMoveHandlers)) {
    node.on(eventDefinition.triggers.join(" "), (event: EventObject) => {
      eventDefinition.action(node, rule, event);
    });
  }
}

/**
 * Adds auto-move handlers to all nodes, so that their children nodes are dragged along with then.
 *
 * @param cy - The cy instance.
 * @param layout - The layout instance.
 */
export const applyAutoMoveEvents: LayoutHook = (
  cy: CytoCore,
  layout: CyLayout
): void => {
  cy.automove("destroy");
  cy.nodes().forEach((node) => addAutoMoveToNode(cy, layout, node));
};

/**
 * Applies cytoscape event handlers in the layout.
 *
 * @param cy - The cy instance.
 * @param layout - The layout instance.
 */
export const applyCytoEvents: LayoutHook = (
  cy: CytoCore,
  layout: CyLayout
): void => {
  for (const cytoEvent of Object.values(layout.cytoEventHandlers)) {
    const eventName: string = cytoEvent.events.join(" ");
    const selector = cytoEvent.selector;
    const handler = (event: EventObject) => cytoEvent.action(cy, event);

    if (selector === undefined) {
      cy.off(eventName);
      cy.on(eventName, handler);
    } else {
      cy.off(eventName, selector);
      cy.on(eventName, selector, handler);
    }
  }
};

/**
 * Centers on the selected or root node of the graph.
 */
export const centerViewOnNode: LayoutHook = (): void => {
  const selectedArtifacts = selectionStore.selectedArtifact?.id;

  if (!selectedArtifacts) {
    cyStore.zoomReset();
    cyStore.centerNodes();
  } else {
    selectionStore.centerOnArtifacts([selectedArtifacts]);
  }
};

/**
 * Post layout hooks for the artifact tree.
 */
export const DefaultPostLayoutHooks: LayoutHook[] = [
  centerViewOnNode,
  applyAutoMoveEvents,
  applyCytoEvents,
];

/**
 * Post layout hooks for the TIM tree.
 */
export const CreatorPostLayoutHooks: LayoutHook[] = [
  (): void => cyStore.centerNodes(false, "creator"),
  applyCytoEvents,
];
