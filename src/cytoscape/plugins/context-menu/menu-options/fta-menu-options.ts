import { appModule, documentModule } from "@/store";
import { ArtifactData, DocumentType, FTANodeType, MenuItem } from "@/types";

/**
 * The menu item for creating FTA related nodes.
 */
export const ftaMenuItem: MenuItem = {
  id: "add-fta-node",
  content: "Add FTA Node",
  tooltipText: "Create a logical node (e.g. AND / OR)",
  onClickFunction(): void {
    appModule.openArtifactCreatorTo(FTANodeType.AND, true);
  },
  isVisible: (artifactData: ArtifactData | undefined): boolean => {
    if (artifactData === undefined) {
      return documentModule.type === DocumentType.FTA;
    }
    return false;
  },
  submenu: [
    {
      id: "fta-and-node",
      content: "AND",
      tooltipText: "Asserts all conditions must be met.",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(FTANodeType.AND, true);
      },
    },
    {
      id: "fta-or-node",
      content: "OR",
      tooltipText: "Asserts at least one condition must be met.",
      onClickFunction(): void {
        appModule.openArtifactCreatorTo(FTANodeType.OR, true);
      },
    },
  ],
};
