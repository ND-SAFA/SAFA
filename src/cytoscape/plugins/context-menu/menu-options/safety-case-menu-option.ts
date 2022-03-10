import { MenuItem } from "@/types/cytoscape/plugins/context-menus";
import { EventObject } from "cytoscape";
import { documentModule, logModule } from "@/store";
import { ArtifactData, DocumentType } from "@/types";

/**
 * The menu option for creating safety case artifacts.
 */
export const safetyCaseMenuOption: MenuItem = {
  id: "add-sc-node",
  content: "Add Safety Case Node",
  tooltipText: "Goal, Solution, Context, Evidence",
  onClickFunction: (event: EventObject): void => {
    logModule.onWarning("Adding Safety Case Nodes is in development.");
  },
  isVisible: (artifactData: ArtifactData | undefined): boolean => {
    if (artifactData === undefined) {
      return documentModule.document.type === DocumentType.SAFETY_CASE;
    }
    return false;
  },
  submenu: [
    {
      id: "sc-goal-node",
      content: "Goal Node",
      tooltipText: "Asserts all conditions must be met.",
      onClickFunction: (event: EventObject): void => {
        logModule.onWarning("Adding Goal nodes is in development.");
      },
    },
    {
      id: "sc-solution-node",
      content: "Solution Node",
      tooltipText: "Depicts the safety strategy of argument",
      onClickFunction: (event: EventObject): void => {
        logModule.onWarning("Adding Solution nodes is in development.");
      },
    },
    {
      id: "sc-context-node",
      content: "Context Node",
      tooltipText: "Expected system environment assumptions",
      onClickFunction: (event: EventObject): void => {
        logModule.onWarning("Adding Context nodes is in development.");
      },
    },
    {
      id: "sc-evidence-node",
      content: "Evidence Node",
      tooltipText: "Container for ground-truth resources",
      onClickFunction: (event: EventObject): void => {
        logModule.onWarning("Adding Evidence nodes is in development.");
      },
    },
  ],
};
