import { NodeSingular, EdgeDataDefinition } from "cytoscape";

/**
 * Defines options for the edge handler.
 */
export interface EdgeHandlersOptions {
  /**
   * Returns whether the source and target can be connected.
   *
   * @param source - The source node.
   * @param target - The target node.
   *
   * @return Whether the nodes can be connected.
   */
  canConnect(source: NodeSingular, target: NodeSingular): boolean;
  /**
   * Returns the edge definition from the source to the target node.
   *
   * @param source - The source node.
   * @param target - The target node.
   *
   * @return The edge definition
   */
  edgeParams(source: NodeSingular, target: NodeSingular): EdgeDataDefinition;
  /**
   * The time spent hovering over a target node before it is considered selected.
   */
  hoverDelay: number;
  /**
   * When enabled, the edge can be drawn by just moving close to a target node.
   * This can be confusing on compound graphs.
   */
  snap: boolean;
  /**
   * The target node must be less than or equal to this many pixels away from the cursor/finger.
   */
  snapThreshold: number;
  /**
   * The number of times per second (Hz) that snap checks done (lower is less expensive).
   */
  snapFrequency: number;
  /**
   * Set events:no to edges during draws, prevents mouseouts on compounds.
   */
  noEdgeEventsInDraw: boolean;
  /**
   * During an edge drawing gesture, disable browser gestures such as two-finger trackpad swipe and pinch-to-zoom.
   */
  disableBrowserGestures: boolean;
}

/**
 * Defines the edge handler callbacks.
 */
export interface EdgeHandleCore {
  /**
   * Called when an edge creation is first started.
   *
   * @param source - The node that the edge is coming from.
   */
  start(source: NodeSingular): void;
  /**
   * Called when the edge creation is stopped.
   */
  stop(): void;
  /**
   * Called to enable edge creation.
   */
  enable(): void;
  /**
   * Called to disable edge creation.
   */
  disable(): void;
  /**
   * Called to enable edge drawing.
   */
  enableDrawMode(): void;
  /**
   * Called to disable edge drawing.
   */
  disableDrawMode(): void;
  /**
   * Called to destroy this edge handler.
   */
  destroy(): void;
}
