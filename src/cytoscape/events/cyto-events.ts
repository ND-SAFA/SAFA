import { CSSCursor, CytoEvent, CytoEventHandlers } from "@/types";

/**
 * Handlers for mouse events on the graph.
 */
export const DefaultCytoEvents: CytoEventHandlers = {
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
      document.body.style.cursor = CSSCursor.GRABBING;
    },
  },
  setDragFreeCursor: {
    events: [CytoEvent.DRAG_FREE, CytoEvent.FREE],
    selector: "node",
    action: () => {
      document.body.style.cursor = CSSCursor.AUTO;
    },
  },
};
