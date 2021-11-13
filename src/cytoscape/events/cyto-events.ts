import { CSSCursor, CytoCore, CytoEvent, CytoEventHandlers } from "@/types";
import { artifactSelectionModule } from "@/store";
import { EventObject } from "cytoscape";

export const DefaultCytoEventHandlers: CytoEventHandlers = {
  mouseOverCursor: {
    events: [CytoEvent.MOUSE_OVER],
    selector: "node",
    action: () => {
      document.body.style.cursor = CSSCursor.POINTER;
    },
  },
  mouseOutCursor: {
    events: [CytoEvent.MOUSE_OUT],
    selector: "node",
    action: () => {
      document.body.style.cursor = CSSCursor.AUTO;
    },
  },

  setDragCursor: {
    events: [CytoEvent.DRAG],
    selector: "node",
    action: () => {
      document.body.style.cursor = "grabbing";
    },
  },
  setDragFreeCursor: {
    events: [CytoEvent.DRAG_FREE, CytoEvent.FREE],
    selector: "node",
    action: () => {
      document.body.style.cursor = "auto";
    },
  },
  unselectArtifactOnBackgroundClick: {
    events: [CytoEvent.TAP],
    action: (cy: CytoCore, event: EventObject) => {
      if (event.target === cy) {
        artifactSelectionModule.clearSelections();
      }
    },
  },
};
