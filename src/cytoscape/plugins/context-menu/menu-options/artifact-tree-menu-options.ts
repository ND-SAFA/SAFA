import { EventObject } from "cytoscape";
import { Artifact, ArtifactData, MenuItem } from "@/types";
import {
  appModule,
  artifactModule,
  artifactSelectionModule,
  logModule,
  projectModule,
  subtreeModule,
  viewportModule,
} from "@/store";
import { enableDrawMode } from "@/cytoscape";
import { handleDeleteArtifact, handleDuplicateArtifact } from "@/api";
import { ftaMenuItem } from "./fta-menu-options";
import { safetyCaseMenuOption } from "./safety-case-menu-option";

/**
 * List of menu items
 */
export const artifactTreeMenuItems: MenuItem[] = [
  {
    id: "add-artifact",
    content: "Add Artifact",
    tooltipText: "Create a new artifact",
    coreAsWell: true,
    onClickFunction(): void {
      if (projectModule.isProjectDefined) {
        appModule.openArtifactCreatorTo({ isNewArtifact: true });
      } else {
        logModule.onWarning("Please select a project to create artifacts.");
      }
    },
    isVisible: () => true,
  },
  {
    id: "add-link",
    content: "Add Link",
    tooltipText: "Create a new trace link",
    coreAsWell: true,
    hasTrailingDivider: true,
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
    tooltipText: "View details about this artifact",
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
    id: "view-body",
    content: "View Body",
    tooltipText: "View this artifact's body text",
    selector: "node",
    coreAsWell: false,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, (artifact: Artifact) => {
        artifactSelectionModule.selectArtifact(artifact.id);
        appModule.SET_ARTIFACT_BODY(true);
      });
    },
    isVisible(artifactData: ArtifactData | undefined): boolean {
      return artifactData !== undefined;
    },
  },
  {
    id: "edit-artifact",
    content: "Edit Artifact",
    tooltipText: "Edit this artifact",
    selector: "node",
    coreAsWell: false,
    hasTrailingDivider: true,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, async (artifact: Artifact) => {
        artifactSelectionModule.selectArtifact(artifact.id);
        appModule.openArtifactCreatorTo({});
      });
    },
    isVisible(artifactData: ArtifactData | undefined): boolean {
      return artifactData !== undefined;
    },
  },
  {
    id: "delete-artifact",
    content: "Delete Artifact",
    tooltipText: "Delete this artifact",
    selector: "node",
    coreAsWell: false,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, async (artifact: Artifact) => {
        await handleDeleteArtifact(artifact, {});
      });
    },
    isVisible(artifactData: ArtifactData | undefined): boolean {
      return artifactData !== undefined;
    },
  },
  {
    id: "duplicate-artifact",
    content: "Duplicate Artifact",
    tooltipText: "Create an identical version of this artifact",
    selector: "node",
    coreAsWell: false,
    hasTrailingDivider: true,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, async (artifact: Artifact) => {
        await handleDuplicateArtifact(artifact, {});
      });
    },
    isVisible(artifactData: ArtifactData | undefined): boolean {
      return artifactData !== undefined;
    },
  },
  {
    id: "highlight-artifact-subtree",
    content: "Highlight Subtree",
    tooltipText: "Highlight this artifact's subtree nodes",
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
    tooltipText: "Hide all child nodes of this artifact",
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
    tooltipText: "Display all child nodes of this artifact",
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
