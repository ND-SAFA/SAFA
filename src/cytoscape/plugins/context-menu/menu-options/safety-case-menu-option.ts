import { MenuItem } from "@/types/cytoscape/plugins/context-menus";
import { appModule, documentModule } from "@/store";
import { ArtifactData, DocumentType, SafetyCaseType } from "@/types";

/**
 * The menu option for creating safety case artifacts.
 */
export const safetyCaseMenuOption: MenuItem = {
  id: "add-sc-node",
  content: "Add Safety Case Node",
  tooltipText: "Goal, Solution, Context, Evidence",
  onClickFunction(): void {
    appModule.openArtifactCreatorTo({
      type: SafetyCaseType.GOAL,
      isNewArtifact: true,
    });
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
        appModule.openArtifactCreatorTo({
          type: SafetyCaseType.GOAL,
          isNewArtifact: true,
        });
      },
    },
    {
      id: "sc-strategy-node",
      content: "Strategy Node",
      tooltipText: "Define the safety strategy of an argument.",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo({
          type: SafetyCaseType.STRATEGY,
          isNewArtifact: true,
        });
      },
    },
    {
      id: "sc-context-node",
      content: "Context Node",
      tooltipText: "Define the expected system environment assumptions.",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo({
          type: SafetyCaseType.CONTEXT,
          isNewArtifact: true,
        });
      },
    },
    {
      id: "sc-evidence-node",
      content: "Evidence Node",
      tooltipText: "Define a container for ground-truth resources.",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo({
          type: SafetyCaseType.SOLUTION,
          isNewArtifact: true,
        });
      },
    },
  ],
};
