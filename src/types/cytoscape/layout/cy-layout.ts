import { LayoutHook } from "@/types/cytoscape/plugins";

/**
 * Defines the layout and event handlers of a graph.
 */
export interface CyLayout {
  preLayoutHooks: LayoutHook[];
  postLayoutHooks: LayoutHook[];
}
