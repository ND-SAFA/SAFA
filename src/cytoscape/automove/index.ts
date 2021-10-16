import { AutoMoveRule } from "@/types/cytoscape/automove";
import { CytoEvent } from "@/types/cytoscape";
import { CSSCursor } from "@/types/cytoscape/cursor";
import { NodeSingular, EventObject } from "cytoscape";

export type AutoMoveNodeEvent = (
  node: NodeSingular,
  rule: AutoMoveRule,
  event: EventObject
) => void;

export interface AutoMoveEventDefinition {
  triggers: CytoEvent[];
  action: AutoMoveNodeEvent;
}
export type AutoMoveEventHandlers = Record<string, AutoMoveEventDefinition>;

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
