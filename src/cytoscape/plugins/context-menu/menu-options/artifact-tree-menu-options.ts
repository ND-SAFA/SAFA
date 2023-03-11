import { EventObject } from "cytoscape";
import { ArtifactSchema, ArtifactCytoElementData, MenuItem } from "@/types";
import {
  appStore,
  artifactStore,
  subtreeStore,
  projectStore,
  selectionStore,
  layoutStore,
  sessionStore,
} from "@/hooks";
import { handleDeleteArtifact, handleDuplicateArtifact } from "@/api";
import { enableDrawMode } from "@/cytoscape/plugins";
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
    isVisible(): boolean {
      return sessionStore.isEditor(projectStore.project);
    },
  },
  {
    id: "add-link",
    content: "Add Link",
    tooltipText: "Create a new trace link",
    coreAsWell: true,
    onClickFunction(): void {
      projectStore.ifProjectDefined(() => {
        appStore.openDetailsPanel("saveTrace");
      });
    },
    isVisible(): boolean {
      return sessionStore.isEditor(projectStore.project);
    },
  },
  {
    id: "draw-link",
    content: "Draw Link",
    tooltipText: "Draw a new trace link between artifacts",
    coreAsWell: true,
    onClickFunction(): void {
      projectStore.ifProjectDefined(() => {
        enableDrawMode();
      });
    },
    isVisible(): boolean {
      return sessionStore.isEditor(projectStore.project);
    },
  },
  {
    id: "generate-link",
    content: "Generate Links",
    tooltipText: "Generate new trace links between artifact levels",
    coreAsWell: true,
    hasTrailingDivider: true,
    onClickFunction(): void {
      projectStore.ifProjectDefined(() => {
        appStore.openDetailsPanel("generateTrace");
      });
    },
    isVisible(): boolean {
      return sessionStore.isEditor(projectStore.project);
    },
  },
  {
    id: "view-artifact",
    content: "View Artifact",
    tooltipText: "View details about this artifact",
    selector: "node",
    coreAsWell: false,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, (artifact: ArtifactSchema) => {
        selectionStore.selectArtifact(artifact.id);
      });
    },
    isVisible(artifactData: ArtifactCytoElementData | undefined): boolean {
      return artifactData !== undefined;
    },
  },
  {
    id: "view-body",
    content: "View Body",
    tooltipText: "View this artifact's body text",
    selector: "node",
    coreAsWell: false,
    hasTrailingDivider: true,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, (artifact: ArtifactSchema) => {
        selectionStore.selectArtifact(artifact.id);
        appStore.openDetailsPanel("displayArtifactBody");
      });
    },
    isVisible(artifactData: ArtifactCytoElementData | undefined): boolean {
      return artifactData !== undefined;
    },
  },
  {
    id: "edit-artifact",
    content: "Edit Artifact",
    tooltipText: "Edit this artifact",
    selector: "node",
    coreAsWell: false,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, async (artifact: ArtifactSchema) => {
        selectionStore.selectArtifact(artifact.id);
        appStore.openArtifactCreatorTo({});
      });
    },
    isVisible(artifactData: ArtifactCytoElementData | undefined): boolean {
      return (
        artifactData !== undefined &&
        sessionStore.isEditor(projectStore.project)
      );
    },
  },
  {
    id: "delete-artifact",
    content: "Delete Artifact",
    tooltipText: "Delete this artifact",
    selector: "node",
    coreAsWell: false,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, async (artifact: ArtifactSchema) => {
        handleDeleteArtifact(artifact, {});
      });
    },
    isVisible(artifactData: ArtifactCytoElementData | undefined): boolean {
      return (
        artifactData !== undefined &&
        sessionStore.isEditor(projectStore.project)
      );
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
      handleOnClick(event, async (artifact: ArtifactSchema) => {
        await handleDuplicateArtifact(artifact, {});
      });
    },
    isVisible(artifactData: ArtifactCytoElementData | undefined): boolean {
      return (
        artifactData !== undefined &&
        sessionStore.isEditor(projectStore.project)
      );
    },
  },
  {
    id: "highlight-subtree",
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
    id: "hide-subtree",
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
    id: "show-subtree",
    content: "Show Subtree",
    tooltipText: "Display all child nodes of this artifact",
    selector: "node",
    async onClickFunction(event: EventObject): Promise<void> {
      const artifactId: string = event.target.data().id;

      await subtreeStore.showSubtree(artifactId);
    },
    isVisible(artifactData: ArtifactCytoElementData | undefined): boolean {
      if (artifactData !== undefined) {
        return subtreeStore.collapsedParentNodes.includes(artifactData.id);
      }
      return false;
    },
  },
  ftaMenuItem,
  safetyCaseMenuOption,
];

/**
 * Determines whether an artifact node has a subtree.
 * @param artifactData - The artifact data to check.
 * @return Whether the artifact has a subtree.
 */
function hasSubtree(artifactData?: ArtifactCytoElementData): boolean {
  if (!artifactData) return false;

  return !subtreeStore.collapsedParentNodes.includes(artifactData.id);
}

/**
 * Handles an artifact on click event.
 * @param event - The event,
 * @param handler - The handler to call with the event's artifact.
 */
function handleOnClick(
  event: EventObject,
  handler: (artifact: ArtifactSchema) => void
): void {
  if (event.target !== null) {
    const artifactData: ArtifactCytoElementData = event.target.data();
    const artifact = artifactStore.getArtifactById(artifactData.id);

    if (!artifact) return;

    handler(artifact);
  }
}
