import { EventObject } from "cytoscape";
import { CytoCore, CytoEvent, CytoEventHandlers } from "@/types/cytoscape/core";
import { ArtifactModel } from "@/types";
import { selectionStore } from "@/hooks";
import { DefaultCytoEvents } from "@/cytoscape/events/cyto-events";
import { disableDrawMode } from "@/cytoscape";

const doubleClickDelayMs = 350;
let previousTapStamp = doubleClickDelayMs;

/**
 * Handlers for mouse events on the artifact tree.
 */
export const ArtifactTreeCytoEvents: CytoEventHandlers = {
  ...DefaultCytoEvents,
  unselectArtifactOnBackgroundClick: {
    events: [CytoEvent.TAP],
    action: (cy: CytoCore, event: EventObject) => {
      if (event.target === cy) {
        selectionStore.clearSelections();
        disableDrawMode();
      }
    },
  },
  select: {
    events: [CytoEvent.TAP],
    action: (cy: CytoCore, event: EventObject) => {
      const currentTimeStamp = event.timeStamp;
      const artifact = event.target.data() as ArtifactModel;
      const msFromLastTap = currentTimeStamp - previousTapStamp;

      if (msFromLastTap === 0 || !artifact.id) return;

      if (msFromLastTap < doubleClickDelayMs) {
        selectionStore.toggleSelectArtifact(artifact.id);
      }

      previousTapStamp = currentTimeStamp;
    },
  },
  selectAll: {
    events: [CytoEvent.BOX_SELECT],
    action: (cy: CytoCore, event: EventObject) => {
      const artifact = event.target.data() as ArtifactModel;

      selectionStore.addToSelectedGroup(artifact.id);
    },
  },
};
