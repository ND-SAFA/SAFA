import {
  ArtifactCytoElementData,
  DocumentType,
  FTANodeType,
  MenuItem,
} from "@/types";
import { appStore, documentStore } from "@/hooks";

/**
 * The menu item for creating FTA related nodes.
 */
export const ftaMenuItem: MenuItem = {
  id: "add-fta-node",
  content: "Add FTA Node",
  tooltipText: "Create a logical node (e.g. AND / OR)",
  onClickFunction(): void {
    appStore.openArtifactCreatorTo({
      type: FTANodeType.AND,
      isNewArtifact: true,
    });
  },
  isVisible: (artifactData: ArtifactCytoElementData | undefined): boolean => {
    if (artifactData === undefined) {
      return documentStore.currentType === DocumentType.FTA;
    }
    return false;
  },
  submenu: [
    {
      id: "fta-and-node",
      content: "AND",
      tooltipText: "Asserts all conditions must be met.",
      onClickFunction(): void {
        appStore.openArtifactCreatorTo({
          type: FTANodeType.AND,
          isNewArtifact: true,
        });
      },
    },
    {
      id: "fta-or-node",
      content: "OR",
      tooltipText: "Asserts at least one condition must be met.",
      onClickFunction(): void {
        appStore.openArtifactCreatorTo({
          type: FTANodeType.OR,
          isNewArtifact: true,
        });
      },
    },
  ],
};
