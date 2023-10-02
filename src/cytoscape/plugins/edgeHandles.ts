import { EdgeHandlersOptions } from "@/types";

/**
 * Options for the edge handlers plugin.
 */
export const EDGE_HANDLERS_OPTIONS: Omit<
  EdgeHandlersOptions,
  "canConnect" | "edgeParams"
> = {
  hoverDelay: 0,
  snap: true,
  snapThreshold: 50,
  snapFrequency: 15,
  noEdgeEventsInDraw: true,
  disableBrowserGestures: true,
};
