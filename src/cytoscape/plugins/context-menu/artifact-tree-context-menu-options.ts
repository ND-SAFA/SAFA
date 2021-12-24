import { EventObject } from "cytoscape";
import {
  logModule,
  artifactSelectionModule,
  projectModule,
  subtreeModule,
  viewportModule,
  appModule,
} from "@/store";
import { PanelType, Artifact, ArtifactData } from "@/types";
import { enableDrawMode } from "@/cytoscape/plugins";
import { deleteArtifactFromCurrentVersion } from "@/api";

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
          await artifactSelectionModule.selectArtifact(artifact);
        }).then();
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
        }).then();
      },
    },
    {
      id: "highlight-artifact-subtree",
      content: "Highlight Subtree",
      tooltipText: "Highlight Subtree",
      selector: "node",
      coreAsWell: false,
      onClickFunction: (thing: EventObject): void => {
        handleOnClick(thing, viewportModule.viewArtifactSubtree).then();
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

async function handleOnClick(
  event: EventObject,
  handler: ArtifactHandler
): Promise<void> {
  if (event.target !== null) {
    const artifactData: ArtifactData = event.target.data();
    const artifact = projectModule.getArtifactByName(artifactData.artifactName);
    await handler(artifact);
  }
}
