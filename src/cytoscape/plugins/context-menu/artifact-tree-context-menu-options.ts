import { EventObject } from "cytoscape";
import {
  logModule,
  artifactSelectionModule,
  projectModule,
  subtreeModule,
  viewportModule,
  appModule,
  artifactModule,
} from "@/store";
import { PanelType, Artifact, ArtifactData } from "@/types";
import { enableDrawMode } from "@/cytoscape/plugins";
import { deleteArtifactFromCurrentVersion } from "@/api";

/**
 * Defines the options on the artifact tree context menu.
 */
export const artifactTreeContextMenuOptions = {
  // Customize event to bring up the context menu
  // Possible options https://js.cytoscape.org/#events/user-input-device-events
  evtType: "cxttap",
  // List of initial menu items
  // A menu item must have either onClickFunction or submenu or both
  menuItems: [
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
      onClickFunction: (thing: EventObject): void => {
        handleOnClick(thing, async (artifact: Artifact) => {
          await artifactSelectionModule.selectArtifact(artifact.id);
        });
      },
    },
    {
      id: "delete-artifact",
      content: "Delete Artifact",
      tooltipText: "Delete Artifact",
      selector: "node",
      coreAsWell: false,
      onClickFunction: (thing: EventObject): void => {
        handleOnClick(thing, async (artifact: Artifact) => {
          await deleteArtifactFromCurrentVersion(artifact);
        });
      },
    },
    {
      id: "highlight-artifact-subtree",
      content: "Highlight Subtree",
      tooltipText: "Highlight Subtree",
      selector: "node",
      coreAsWell: false,
      onClickFunction: (thing: EventObject): void => {
        handleOnClick(thing, viewportModule.viewArtifactSubtree);
      },
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
    },
  ],
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
