import { EventObject } from "cytoscape";
import {
  appModule,
  artifactSelectionModule,
  projectModule,
  viewportModule,
} from "@/store";
import { PanelType, Artifact, ArtifactData } from "@/types";
import { enableDrawMode } from "@/cytoscape/plugins";
import { deleteArtifactHandler } from "@/api";

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
      onClickFunction: () => {
        if (projectModule.isProjectDefined) {
          appModule.openPanel(PanelType.artifactCreator);
        } else {
          appModule.onWarning("Please select a project to create artifacts.");
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
          appModule.onWarning("Please select a project to create trace links.");
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
          artifactSelectionModule.selectArtifact(artifact);
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
          const projectId = projectModule.getProject.projectId;
          deleteArtifactHandler(projectId, artifact.name).then();
        }).then();
      },
    },
    {
      id: "view-artifact-subtree",
      content: "Highlight Subtree",
      tooltipText: "View Subtree",
      selector: "node",
      coreAsWell: false,
      onClickFunction: (thing: EventObject): void => {
        handleOnClick(thing, viewportModule.viewArtifactSubtree).then();
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
    if (artifact !== undefined) {
      await handler(artifact);
    }
  }
}
