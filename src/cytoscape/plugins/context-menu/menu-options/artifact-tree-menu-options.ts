import { EventObject } from "cytoscape";
import { ArtifactModel, ArtifactData, MenuItem } from "@/types";
import {
  appStore,
  artifactStore,
  subtreeStore,
  projectStore,
  selectionStore,
  layoutStore,
} from "@/hooks";
import { enableDrawMode } from "@/cytoscape";
import { handleDeleteArtifact, handleDuplicateArtifact } from "@/api";
import { safetyCaseMenuOption } from "./safety-case-menu-option";
import { ftaMenuItem } from "./fta-menu-options";

/**
 * List of menu items
 */
export const artifactTreeMenuItems: MenuItem[] = [
  {
    id: "add-artifact",
    content: "Add Artifact",
    tooltipText: "Create a new artifact",
    coreAsWell: true,
    onClickFunction(event: EventObject): void {
      projectStore.ifProjectDefined(() => {
        layoutStore.savedPosition = event.position;
        appStore.openArtifactCreatorTo({ isNewArtifact: true });
      });
    },
    isVisible: () => true,
  },
  {
    id: "add-link",
    content: "Add Link",
    tooltipText: "Create a new trace link",
    coreAsWell: true,
    onClickFunction(): void {
      projectStore.ifProjectDefined(() => {
        appStore.toggleTraceLinkCreator();
      });
    },
  },
  {
    id: "draw-link",
    content: "Draw Link",
    tooltipText: "Draw a new trace link between artifacts",
    coreAsWell: true,
    hasTrailingDivider: true,
    onClickFunction(): void {
      projectStore.ifProjectDefined(() => {
        enableDrawMode();
      });
    },
  },
  {
    id: "view-artifact",
    content: "View Artifact",
    tooltipText: "View details about this artifact",
    selector: "node",
    coreAsWell: false,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, (artifact: ArtifactModel) => {
        selectionStore.selectArtifact(artifact.id);
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
      handleOnClick(event, (artifact: ArtifactModel) => {
        selectionStore.selectArtifact(artifact.id);
        appStore.toggleArtifactBody();
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
      handleOnClick(event, async (artifact: ArtifactModel) => {
        selectionStore.selectArtifact(artifact.id);
        appStore.openArtifactCreatorTo({});
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
      handleOnClick(event, async (artifact: ArtifactModel) => {
        handleDeleteArtifact(artifact, {});
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
      handleOnClick(event, async (artifact: ArtifactModel) => {
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
      handleOnClick(event, ({ id }) => selectionStore.viewArtifactSubtree(id));
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

      await subtreeStore.hideSubtree(artifactId);
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

      await subtreeStore.showSubtree(artifactId);
    },
    isVisible(artifactData: ArtifactData | undefined): boolean {
      if (artifactData !== undefined) {
        return subtreeStore.collapsedParentNodes.includes(artifactData.id);
      }
      return false;
    },
  },
  ftaMenuItem,
  safetyCaseMenuOption,
];

function hasSubtree(artifactData: ArtifactData | undefined): boolean {
  if (artifactData !== undefined) {
    return !subtreeStore.collapsedParentNodes.includes(artifactData.id);
  }
  return false;
}

type ArtifactHandler = (a: ArtifactModel) => void | Promise<void>;

/**
 * Handles an artifact on click event.
 * @param event - The event,
 * @param handler - The handler to call with the event's artifact.
 */
function handleOnClick(event: EventObject, handler: ArtifactHandler): void {
  if (event.target !== null) {
    const artifactData: ArtifactData = event.target.data();
    const artifact = artifactStore.getArtifactById(artifactData.id);

    if (!artifact) return;

    handler(artifact);
  }
}
