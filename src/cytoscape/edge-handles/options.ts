import store, { projectModule } from "@/store";
import { EdgeHandlersOptions } from "@/types/cytoscape/edge-handles";
import { getTraceId } from "@/util/trace-helper";
import { NodeSingular, EdgeDataDefinition } from "cytoscape";

// the default values of each option are outlined below:
export const edgeHandleOptions: EdgeHandlersOptions = {
  /**
   * Return whether any two nodes can be traced. Criteria includes:
   * - source != target
   * - trace link between source and target doesn't already exist.
   * @param source
   * @param target
   * @returns
   */
  canConnect(source: NodeSingular, target: NodeSingular): boolean {
    if (source.data() === undefined || target.data() === undefined) {
      return false;
    }
    const doesLinkExist: boolean = projectModule.doesLinkExist(
      source.data().id,
      target.data().id
    );
    return !doesLinkExist && !source.same(target); // e.g. disallow loops
  },

  /**
   * Handler that determines the data to be added to cytoscape upon the edge snap
   * to a target node.
   * @param source
   * @param target
   * @returns
   */
  edgeParams(
    sourceNode: NodeSingular,
    targetNode: NodeSingular
  ): EdgeDataDefinition {
    const source: string = sourceNode.data().id;
    const target: string = targetNode.data().id;
    return { id: getTraceId(source, target), source, target };
  },
  hoverDelay: 0,
  // time spent hovering over a target node before it is considered selected
  snap: true, // when enabled, the edge can be drawn by just moving close to a target node (can be confusing on compound graphs)
  snapThreshold: 50, // the target node must be less than or equal to this many pixels away from the cursor/finger
  snapFrequency: 15, // the number of times per second (Hz) that snap checks done (lower is less expensive)
  noEdgeEventsInDraw: true, // set events:no to edges during draws, prevents mouseouts on compounds
  disableBrowserGestures: true, // during an edge drawing gesture, disable browser gestures such as two-finger trackpad swipe and pinch-to-zoom
};
