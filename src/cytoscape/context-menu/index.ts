import {
  appModule,
  artifactSelectionModule,
  projectModule,
  viewportModule,
} from "@/store";
import { PanelType } from "@/types/store";
import { enableDrawMode } from "@/cytoscape/edge-handles";
import { EventObject } from "cytoscape";
import { Artifact, ArtifactData } from "@/types/domain/artifact";

export const contextMenuOptions = {
  // Customize event to bring up the context menu
  // Possible options https://js.cytoscape.org/#events/user-input-device-events
  evtType: "cxttap",
  // List of initial menu items
  // A menu item must have either onClickFunction or submenu or both
  menuItems: [
    {
      id: "add-node",
      content: "Add Artifact",
      tooltipText: "Create new artifact",
      selector: "node",
      coreAsWell: true,
      onClickFunction: (): void =>
        appModule.openPanel(PanelType.artifactCreator),
    },
    {
      id: "view-artifact",
      content: "View Artifact",
      tooltipText: "View Artifact",
      selector: "node",
      coreAsWell: true,
      onClickFunction: (thing: EventObject): void => {
        handleOnClick(thing, async (artifact: Artifact) => {
          artifactSelectionModule.selectArtifact(artifact);
          appModule.openPanel(PanelType.left);
        });
      },
    },
    {
      id: "view-artifact-subtree",
      content: "View Subtree",
      tooltipText: "View Subtree",
      selector: "node",
      coreAsWell: true,
      onClickFunction: (thing: EventObject): void => {
        handleOnClick(thing, viewportModule.viewArtifactSubtree);
      },
    },
    {
      id: "add-link",
      content: "Add Link",
      tooltipText: "Create new trace link",
      selector: "edge",
      coreAsWell: true,
      onClickFunction: (): void => enableDrawMode(),
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
