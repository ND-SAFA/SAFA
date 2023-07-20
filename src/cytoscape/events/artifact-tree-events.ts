import { EventObject } from "cytoscape";
import { ArtifactCytoElementData, DetailsOpenState } from "@/types";
import { appStore, selectionStore } from "@/hooks";
import { disableDrawMode } from "@/cytoscape/plugins";
import { DefaultCytoEvents } from "@/cytoscape/events/cyto-events";
import { CytoCore, CytoEvent, CytoEventHandlers } from "@/types/cytoscape/core";

/**
 * Handlers for mouse events on the artifact tree.
 */
export const ArtifactTreeCytoEvents: CytoEventHandlers = {
  ...DefaultCytoEvents,
  unselectArtifactOnBackgroundClick: {
    events: [CytoEvent.TAP],
    action(cy: CytoCore, event: EventObject) {
      if (event.target !== cy) return;

      disableDrawMode();

      // Don't close the side panels if an object is being edited.
      if (
        (
          ["document", "saveArtifact", "saveTrace"] as DetailsOpenState[]
        ).includes(appStore.isDetailsPanelOpen)
      )
        return;

      selectionStore.clearSelections(true);
    },
  },
  selectAllArtifacts: {
    events: [CytoEvent.BOX_SELECT],
    action(cy: CytoCore, event: EventObject) {
      const artifact = event.target.data() as ArtifactCytoElementData;

      selectionStore.addToSelectedGroup(artifact.id);
    },
  },
};
