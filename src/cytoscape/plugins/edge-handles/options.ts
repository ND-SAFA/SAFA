import { NodeSingular, EdgeDataDefinition } from "cytoscape";
import { EdgeHandlersOptions } from "@/types";
import { getTraceId } from "@/util";
import { canConnect } from "@/cytoscape/plugins/edge-handles/can-connect";

// the default values of each option are outlined below:
export const artifactTreeEdgeHandleOptions: EdgeHandlersOptions = {
  canConnect,

  /**
   * Handler that determines the data to be added to cytoscape upon the edge snap
   * to a target node.
   *
   * @param sourceNode - The source node on the graph.
   * @param targetNode - The target node on the graph.
   * @returns The created edge.
   */
  edgeParams(
    sourceNode: NodeSingular,
    targetNode: NodeSingular
  ): EdgeDataDefinition {
    const source: string = sourceNode.data().id;
    const target: string = targetNode.data().id;

    return { id: getTraceId(source, target), source, target };
  },

  // time spent hovering over a target node before it is considered selected.
  hoverDelay: 0,
  // when enabled, the edge can be drawn by just moving close to a target node (can be confusing on compound graphs).
  snap: true,
  // the target node must be less than or equal to this many pixels away from the cursor/finger.
  snapThreshold: 50,
  // the number of times per second (Hz) that snap checks done (lower is less expensive).
  snapFrequency: 15,
  // set events:no to edges during draws, prevents mouseouts on compounds.
  noEdgeEventsInDraw: true,
  // during an edge drawing gesture, disable browser gestures such as two-finger trackpad swipe and pinch-to-zoom.
  disableBrowserGestures: true,
};
