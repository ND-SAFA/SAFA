import { EventObject } from "cytoscape";
import { documentModule, logModule } from "@/store";
import { ArtifactData, DocumentType } from "@/types";
import { MenuItem } from "@/types/cytoscape/plugins/context-menus";

/**
 * The menu item for creating FTA related nodes.
 */
export const ftaMenuItem: MenuItem = {
  id: "add-fta-node",
  content: "Add FTA Node",
  tooltipText: "Create a logical node (e.g. AND / OR)",
  onClickFunction: (event: EventObject): void => {
    logModule.onWarning("Adding FTA Nodes is in development.");
  },
  isVisible: (artifactData: ArtifactData | undefined): boolean => {
    if (artifactData === undefined) {
      return documentModule.document.type === DocumentType.FTA;
    }
    return false;
  },
  submenu: [
    {
      id: "fta-and-node",
      content: "AND",
      tooltipText: "Asserts all conditions must be met.",
      onClickFunction: (event: EventObject): void => {
        logModule.onWarning("Adding AND artifacts is in development.");
      },
    },
    {
      id: "fta-or-node",
      content: "OR",
      tooltipText: "Asserts at least one condition must be met.",
      onClickFunction: (event: EventObject): void => {
        logModule.onWarning("Adding OR artifacts is in development.");
      },
    },
  ],
};
