import { projectModule } from "@/store";
import { EdgeHandlersOptions } from "@/types";
import { getTraceId } from "@/util";
import { NodeSingular, EdgeDataDefinition } from "cytoscape";

// the default values of each option are outlined below:
export const artifactTreeEdgeHandleOptions: EdgeHandlersOptions = {
  /**
   * Return whether any two nodes can be traced. Criteria includes:
   * - source != target.
   * - trace link between source and target doesn't already exist.
   *
   * @param sourceNode - The source node on the graph.
   * @param targetNode - The target node on the graph.
   * @returns Whether the two nodes can be traced.
   */
  canConnect(sourceNode: NodeSingular, targetNode: NodeSingular): boolean {
    if (sourceNode.data() === undefined || targetNode.data() === undefined) {
      // If either link doesn't have any data, the link cannot be created.
      return false;
    }

    // If this link already exists, the link cannot be created.
    const linkDoesNotExist = !projectModule.doesLinkExist(
      sourceNode.data().id,
      targetNode.data().id
    );

    // If this link is to itself, the link cannot be created.
    const isNotSameNode = !sourceNode.same(targetNode);

    // If the link is not between allowed artifact directions, thee link cannot be created.
    const linkIsAllowedByType = projectModule.isLinkAllowedByType(
      sourceNode.data().artifactType,
      targetNode.data().artifactType
    );

    return linkDoesNotExist && isNotSameNode && linkIsAllowedByType;
  },

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
