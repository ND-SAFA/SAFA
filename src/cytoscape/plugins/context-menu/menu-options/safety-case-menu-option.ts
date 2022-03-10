import { MenuItem } from "@/types/cytoscape/plugins/context-menus";
import { EventObject } from "cytoscape";
import { appModule, documentModule, logModule } from "@/store";
import { ArtifactData, DocumentType, SafetyCaseType } from "@/types";

/**
 * The menu option for creating safety case artifacts.
 */
export const safetyCaseMenuOption: MenuItem = {
  id: "add-sc-node",
  content: "Add Safety Case Node",
  tooltipText: "Goal, Solution, Context, Evidence",
  onClickFunction(): void {
    appModule.openArtifactCreatorTo(SafetyCaseType.GOAL);
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
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(SafetyCaseType.GOAL);
      },
    },
    {
      id: "sc-solution-node",
      content: "Solution Node",
      tooltipText: "Depicts the safety strategy of argument",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(SafetyCaseType.SOLUTION);
      },
    },
    {
      id: "sc-context-node",
      content: "Context Node",
      tooltipText: "Expected system environment assumptions",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(SafetyCaseType.CONTEXT);
      },
    },
    {
      id: "sc-evidence-node",
      content: "Evidence Node",
      tooltipText: "Container for ground-truth resources",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(SafetyCaseType.STRATEGY);
      },
    },
  ],
};
