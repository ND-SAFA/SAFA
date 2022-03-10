import { CytoEvent } from "@/types";
import { ContextMenuOptions } from "@/types/cytoscape/plugins/context-menus";
import { artifactTreeMenuItems } from "@/cytoscape/plugins/context-menu/menu-options/artifact-tree-menu-options";

/**
 * Defines the options on the artifact tree context menu.
 */
export const artifactTreeContextMenuOptions: ContextMenuOptions = {
  // Customize event to bring up the context menu
  // Possible options https://js.cytoscape.org/#events/user-input-device-events
  evtType: CytoEvent.CXT_TAP,
  // List of initial menu items
  // A menu item must have either onClickFunction or submenu or both
  menuItems: artifactTreeMenuItems,
  // css classes that menu items will have
  menuItemClasses: [], // add class names to this list
  // css classes that context menu will have
  contextMenuClasses: [], // add class names to this list
  submenuIndicator: {
    src: "assets/submenu-indicator-default.svg",
    width: 12,
    height: 12,
  },
};
