import { EventObject, NodeSingular } from "cytoscape";
import {
  LayoutHook,
  AutoMoveReposition,
  CytoCore,
  IGraphLayout,
  CytoEvent,
  ArtifactData,
} from "@/types";
import { artifactSelectionModule, viewportModule } from "@/store";
import { artifactTreeMenuItems, cyCenterNodes, cyZoomReset } from "@/cytoscape";
import { MenuItem } from "@/types/cytoscape/plugins/context-menus";
import { isArtifactData } from "@/util";

/**
 * Adds auto-move handlers to a node, so that its child nodes are dragged along with it.
 *
 * @param cy - The cy instance.
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

/**
 * Adds auto-move handlers to all nodes, so that their children nodes are dragged along with then.
 *
 * @param cy - The cy instance.
 * @param layout - The layout instance.
 */
export const applyAutoMoveEvents: LayoutHook = (
  cy: CytoCore,
  layout: IGraphLayout
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

/**
 * Centers on the selected or root node of the graph.
 */
export const centerViewOnNode: LayoutHook = (): void => {
  const selectedArtifacts = artifactSelectionModule.getSelectedArtifactId;

  if (!selectedArtifacts) {
    cyZoomReset();
    cyCenterNodes();
  } else {
    viewportModule.centerOnArtifacts([selectedArtifacts]);
  }
};

/**
 * Dynamically shows context menu items that are visible at the time of
 * getting called.
 * @param cy
 */
export const dynamicVisibilityHookForContextMenuItems = (
  cy: CytoCore
): void => {
  cy.on(CytoEvent.CXT_TAP, (event: EventObject) => {
    const data = event.target.data();
    const artifactData: ArtifactData | undefined = isArtifactData(data)
      ? data
      : undefined;
    const contextMenuInstance = cy.contextMenus("get");
    artifactTreeMenuItems.forEach((menuItem: MenuItem) => {
      if (
        menuItem.coreAsWell ||
        (menuItem.isVisible !== undefined && menuItem.isVisible(artifactData))
      ) {
        contextMenuInstance.showMenuItem(menuItem.id);
      } else {
        contextMenuInstance.hideMenuItem(menuItem.id);
      }
    });
  });
};

export const DefaultPostLayoutHooks: LayoutHook[] = [
  centerViewOnNode,
  applyAutoMoveEvents,
  applyCytoEvents,
  dynamicVisibilityHookForContextMenuItems,
];
