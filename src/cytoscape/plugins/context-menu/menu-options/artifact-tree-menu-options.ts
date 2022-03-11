import { MenuItem } from "@/types/cytoscape/plugins/context-menus";
import {
  appModule,
  artifactModule,
  artifactSelectionModule,
  logModule,
  projectModule,
  subtreeModule,
  viewportModule,
} from "@/store";
import { Artifact, ArtifactData, PanelType } from "@/types";
import { enableDrawMode } from "@/cytoscape";
import { EventObject } from "cytoscape";
import { deleteArtifactFromCurrentVersion } from "@/api";
import { ftaMenuItem } from "./fta-menu-options";
import { safetyCaseMenuOption } from "./safety-case-menu-option";

/**
 * List of menu items
 */
export const artifactTreeMenuItems: MenuItem[] = [
  {
    id: "add-artifact",
    content: "Add Artifact",
    tooltipText: "Create new artifact",
    coreAsWell: true,
    onClickFunction(): void {
      if (projectModule.isProjectDefined) {
        appModule.openPanel(PanelType.artifactCreator);
      } else {
        logModule.onWarning("Please select a project to create artifacts.");
      }
    },
    isVisible: () => true,
  },
  {
    id: "add-link",
    content: "Add Link",
    tooltipText: "Create new trace link",
    coreAsWell: true,
    onClickFunction(): void {
      if (projectModule.isProjectDefined) {
        enableDrawMode();
      } else {
        logModule.onWarning("Please select a project to create trace links.");
      }
    },
  },
  {
    id: "view-artifact",
    content: "View Artifact",
    tooltipText: "View Artifact",
    selector: "node",
    coreAsWell: false,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, (artifact: Artifact) => {
        artifactSelectionModule.selectArtifact(artifact.id);
      });
    },
    isVisible(artifactData: ArtifactData | undefined): boolean {
      return artifactData !== undefined;
    },
  },
  {
    id: "delete-artifact",
    content: "Delete Artifact",
    tooltipText: "Delete Artifact",
    selector: "node",
    coreAsWell: false,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, async (artifact: Artifact) => {
        await deleteArtifactFromCurrentVersion(artifact);
      });
    },
    isVisible(artifactData: ArtifactData | undefined): boolean {
      return artifactData !== undefined;
    },
  },
  {
    id: "highlight-artifact-subtree",
    content: "Highlight Subtree",
    tooltipText: "Highlight Subtree",
    selector: "node",
    coreAsWell: false,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, viewportModule.viewArtifactSubtree);
    },
    isVisible: hasSubtree,
  },
  {
    id: "hide-artifact-subtree",
    content: "Hide Subtree",
    tooltipText: "Hide all children.",
    selector: "node",
    async onClickFunction(event: EventObject): Promise<void> {
      const artifactId: string = event.target.data().id;

      await subtreeModule.hideSubtree(artifactId);
    },
    isVisible: hasSubtree,
  },
  {
    id: "show-artifact-subtree",
    content: "Show Subtree",
    tooltipText: "Show all hidden children.",
    selector: "node",
    async onClickFunction(event: EventObject): Promise<void> {
      const artifactId: string = event.target.data().id;

      await subtreeModule.showSubtree(artifactId);
    },
    isVisible(artifactData: ArtifactData | undefined): boolean {
      if (artifactData !== undefined) {
        return subtreeModule.getCollapsedParentNodes.includes(artifactData.id);
      }
      return false;
    },
  },
  ftaMenuItem,
  safetyCaseMenuOption,
];

function hasSubtree(artifactData: ArtifactData | undefined): boolean {
  if (artifactData !== undefined) {
    return !subtreeModule.getCollapsedParentNodes.includes(artifactData.id);
  }
  return false;
}

type ArtifactHandler = (a: Artifact) => void | Promise<void>;

/**
 * Handles an artifact on click event.
 * @param event - The event,
 * @param handler - The handler to call with the event's artifact.
 */
function handleOnClick(event: EventObject, handler: ArtifactHandler): void {
  if (event.target !== null) {
    const artifactData: ArtifactData = event.target.data();
    const artifact = artifactModule.getArtifactByName(
      artifactData.artifactName
    );

    handler(artifact);
  }
}
