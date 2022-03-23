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
      return documentModule.type === DocumentType.SAFETY_CASE;
    }
    return false;
  },
  submenu: [
    {
      id: "sc-goal-node",
      content: "Goal Node",
      tooltipText: "Define an expected system property.",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(SafetyCaseType.GOAL);
      },
    },
    {
      id: "sc-strategy-node",
      content: "Strategy Node",
      tooltipText: "Define the safety strategy of an argument.",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(SafetyCaseType.STRATEGY);
      },
    },
    {
      id: "sc-solution-node",
      content: "Solution Node",
      tooltipText: "Define how the system resolves a strategy.",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(SafetyCaseType.SOLUTION);
      },
    },
    {
      id: "sc-context-node",
      content: "Context Node",
      tooltipText: "Define the expected system environment assumptions.",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(SafetyCaseType.CONTEXT);
      },
    },
    {
      id: "sc-evidence-node",
      content: "Evidence Node",
      tooltipText: "Define a container for ground-truth resources.",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(SafetyCaseType.STRATEGY);
      },
    },
  ],
};
