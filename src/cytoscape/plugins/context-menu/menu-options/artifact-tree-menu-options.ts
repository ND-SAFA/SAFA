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
  artifactApiStore,
} from "@/hooks";
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
      layoutStore.savedPosition = event.position;
      appStore.openArtifactCreatorTo({ isNewArtifact: true });
    },
    isVisible: isEditor,
  },
  {
    id: "generate-artifact",
    content: "Generate Artifacts",
    tooltipText: "Generate parent artifacts from other artifacts.",
    coreAsWell: true,
    onClickFunction(): void {
      appStore.openDetailsPanel("generateArtifact");
    },
    isVisible: isEditor,
  },
  {
    id: "add-link",
    content: "Add Link",
    tooltipText: "Create a new trace link",
    coreAsWell: true,
    onClickFunction(): void {
      appStore.openTraceCreatorTo();
    },
    isVisible: isEditor,
  },
  {
    id: "draw-link",
    content: "Draw Link",
    tooltipText: "Draw a new trace link between artifacts",
    coreAsWell: true,
    onClickFunction(): void {
      enableDrawMode();
    },
    isVisible: isEditor,
  },
  {
    id: "generate-link",
    content: "Generate Links",
    tooltipText: "Generate new trace links between artifact levels",
    coreAsWell: true,
    hasTrailingDivider: true,
    onClickFunction(): void {
      appStore.openDetailsPanel("generateTrace");
    },
    isVisible: isEditor,
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
      return !!artifactData;
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
    isVisible: hasValidData,
  },
  {
    id: "delete-artifact",
    content: "Delete Artifact",
    tooltipText: "Delete this artifact",
    selector: "node",
    coreAsWell: false,
    onClickFunction(event: EventObject): void {
      handleOnClick(event, async (artifact: ArtifactSchema) => {
        artifactApiStore.handleDelete(artifact);
      });
    },
    isVisible: hasValidData,
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
        await artifactApiStore.handleDuplicate(artifact);
      });
    },
    isVisible: hasValidData,
  },
  {
    id: "add-link-parent",
    content: "Add Parent",
    tooltipText: "Create a new trace link to a parent",
    selector: "node",
    onClickFunction(event: EventObject): void {
      handleOnClick(event, async (artifact: ArtifactSchema) => {
        appStore.openTraceCreatorTo({
          type: "source",
          artifactId: artifact.id,
        });
      });
    },
    isVisible: hasValidData,
  },
  {
    id: "add-link-child",
    content: "Add Child",
    tooltipText: "Create a new trace link to a child",
    selector: "node",
    onClickFunction(event: EventObject): void {
      handleOnClick(event, async (artifact: ArtifactSchema) => {
        appStore.openTraceCreatorTo({
          type: "target",
          artifactId: artifact.id,
        });
      });
    },
    isVisible: hasValidData,
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
      return artifactData
        ? subtreeStore.collapsedParentNodes.includes(artifactData.id)
        : false;
    },
  },
  ftaMenuItem,
  safetyCaseMenuOption,
];

/**
 * Determines whether a project is loaded & the user is an editor of it.
 */
function isEditor(): boolean {
  return (
    projectStore.isProjectDefined && sessionStore.isEditor(projectStore.project)
  );
}

/**
 * Determines whether an artifact node has valid data.
 * @param artifactData - The artifact data to check.
 * @return Whether the artifact has valid data.
 */
function hasValidData(
  artifactData: ArtifactCytoElementData | undefined
): boolean {
  return !!artifactData && isEditor();
}

/**
 * Determines whether an artifact node has a subtree.
 * @param artifactData - The artifact data to check.
 * @return Whether the artifact has a subtree.
 */
function hasSubtree(artifactData?: ArtifactCytoElementData): boolean {
  return (
    !!artifactData &&
    !subtreeStore.collapsedParentNodes.includes(artifactData.id)
  );
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
