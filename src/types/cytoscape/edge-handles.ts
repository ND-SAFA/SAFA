import { NodeSingular, EdgeDataDefinition } from "cytoscape";

export interface EdgeHandlersOptions {
  canConnect(source: NodeSingular, target: NodeSingular): boolean;
  edgeParams(source: NodeSingular, target: NodeSingular): EdgeDataDefinition;
  // time spent hovering over a target node before it is considered selected
  hoverDelay: number;
  // when enabled, the edge can be drawn by just moving close to a target node (can be confusing on compound graphs)
  snap: boolean;
  // the target node must be less than or equal to this many pixels away from the cursor/finger
  snapThreshold: number;
  // the number of times per second (Hz) that snap checks done (lower is less expensive)
  snapFrequency: number;
  // set events:no to edges during draws, prevents mouseouts on compounds
  noEdgeEventsInDraw: boolean;
  // during an edge drawing gesture, disable browser gestures such as two-finger
  //trackpad swipe and pinch-to-zoom
  disableBrowserGestures: boolean;
}

export interface EdgeHandleCore {
  start(source: NodeSingular): void;
  stop(): void;
  disable(): void;
  enable(): void;
  enableDrawMode(): void;
  disableDrawMode(): void;
  destroy(): void;
}
