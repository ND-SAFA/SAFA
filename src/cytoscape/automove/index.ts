import {
  AutoMoveEventHandlers,
  AutoMoveRule,
  CSSCursor,
  CytoEvent,
} from "@/types";
import { EventObject, NodeSingular } from "cytoscape";

export const DefaultAutoMoveEventHandlers: AutoMoveEventHandlers = {
  onContextDrag: {
    triggers: [CytoEvent.CXT_DRAG],
    action: (node: NodeSingular, rule: AutoMoveRule, event: EventObject) => {
      document.body.style.cursor = CSSCursor.GRAB;
      const nodePosition = event.target.renderedPosition();
      event.target.renderedPosition({
        x: nodePosition.x + event.originalEvent.movementX,
        y: nodePosition.y + event.originalEvent.movementY,
      });
    },
  },
};
