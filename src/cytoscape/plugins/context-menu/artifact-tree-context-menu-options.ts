import { EventObject } from "cytoscape";
import {
  appModule,
  artifactModule,
  artifactSelectionModule,
  logModule,
  projectModule,
  subtreeModule,
  viewportModule,
} from "@/store";
import { Artifact, ArtifactData, CytoEvent, PanelType } from "@/types";
import { enableDrawMode } from "@/cytoscape/plugins";
import { deleteArtifactFromCurrentVersion } from "@/api";
import {
  ContextMenuOptions,
  MenuItem,
} from "@/types/cytoscape/plugins/context-menus";

/**
 * List of menu items
 */
export const artifactTreeMenuItems: MenuItem[] = [
  {
    id: "add-artifact",
    content: "Add Artifact",
    tooltipText: "Create new artifact",
    selector: "node, edge",
    coreAsWell: true,
    onClickFunction: (): void => {
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
    selector: "node",
    coreAsWell: true,
    onClickFunction: (): void => {
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
    onClickFunction: (event: EventObject): void => {
      handleOnClick(event, (artifact: Artifact) => {
        artifactSelectionModule.selectArtifact(artifact.id);
      });
    },
    isVisible: (artifactData: ArtifactData | undefined) => {
      return artifactData !== undefined;
    },
  },
  {
    id: "delete-artifact",
    content: "Delete Artifact",
    tooltipText: "Delete Artifact",
    selector: "node",
    coreAsWell: false,
    onClickFunction: (event: EventObject): void => {
      handleOnClick(event, async (artifact: Artifact) => {
        await deleteArtifactFromCurrentVersion(artifact);
      });
    },
    isVisible: (artifactData: ArtifactData | undefined) => {
      return artifactData !== undefined;
    },
  },
  {
    id: "highlight-artifact-subtree",
    content: "Highlight Subtree",
    tooltipText: "Highlight Subtree",
    selector: "node",
    coreAsWell: false,
    onClickFunction: (event: EventObject): void => {
      handleOnClick(event, viewportModule.viewArtifactSubtree);
    },
    isVisible: hasSubtree,
  },
  {
    id: "hide-artifact-subtree",
    content: "Hide Subtree",
    tooltipText: "Hide all children.",
    selector: "node", //TODO: disable this option if already hidden
    onClickFunction: async (event: EventObject): Promise<void> => {
      const artifactId: string = event.target.data().id;

      await subtreeModule.hideSubtree(artifactId);
    },
    isVisible: hasSubtree,
  },
  {
    id: "show-artifact-subtree",
    content: "Show Subtree",
    tooltipText: "Show all hidden children.",
    selector: "node", //TODO: disable this option if already hidden
    onClickFunction: async (event: EventObject): Promise<void> => {
      const artifactId: string = event.target.data().id;

      await subtreeModule.showSubtree(artifactId);
    },
    isVisible: (artifactData: ArtifactData | undefined) => {
      if (artifactData !== undefined) {
        return subtreeModule.getCollapsedParentNodes.includes(artifactData.id);
      }
      return false;
    },
  },
];

function hasSubtree(artifactData: ArtifactData | undefined): boolean {
  if (artifactData !== undefined) {
    return !subtreeModule.getCollapsedParentNodes.includes(artifactData.id);
  }
  return false;
}

/**
 * Defines the options on the artifact tree context menu.
 */
export const artifactTreeContextMenuOptions: ContextMenuOptions = {
  // Customize event to bring up the context menu
  // Possible options https://js.cytoscape.org/#events/user-input-device-events
  evtType: CytoEvent.CXT_TAP,
  // List of initial menu items
  // A menu item must have either onClickFunction or submenu or both
  menuItems: artifactTreeMenuItems,
  // css classes that menu items will have
  menuItemClasses: [], // add class names to this list
  // css classes that context menu will have
  contextMenuClasses: [], // add class names to this list
};

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
