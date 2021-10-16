import { CytoCore } from "@/types/cytoscape";
import { CytoEvent } from "@/types/cytoscape";
import { CSSCursor } from "@/types/cytoscape/cursor";
import { artifactSelectionModule, viewportModule } from "@/store";
import { EventObject } from "cytoscape";

export interface CytoEventDefinition {
  events: CytoEvent[];
  selector?: string;
  action: (cy: CytoCore, event: EventObject) => void;
}
export type CytoEventHandlers = Record<string, CytoEventDefinition>;

let timeout: NodeJS.Timeout; // used for restricting number of resize events called

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
  onResizeContainer: {
    events: [CytoEvent.RESIZE],
    action: () => {
      clearTimeout(timeout);
      timeout = setTimeout(
        async () => await viewportModule.repositionSelectedSubtree(),
        500
      );
    },
  },
  unselectArtifactOnBackgroundClick: {
    events: [CytoEvent.TAP],
    action: (cy: CytoCore, event: EventObject) => {
      if (event.target === cy) {
        artifactSelectionModule.unselectArtifact();
        artifactSelectionModule
          .filterGraph({
            type: "subtree",
            artifactsInSubtree: [],
          })
          .then();
      }
    },
  },
};
