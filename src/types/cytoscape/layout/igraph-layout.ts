import {
  KlayLayoutSettings,
  LayoutHook,
  AutoMoveEventHandlers,
} from "@/types/cytoscape/plugins";
import { CytoCore, CytoEventHandlers } from "@/types/cytoscape/core";

/**
 * Defines the layout and event handlers of a graph.
 */
export interface IGraphLayout {
  klaySettings: KlayLayoutSettings | undefined;
  preLayoutHooks: LayoutHook[];
  postLayoutHooks: LayoutHook[];
  autoMoveHandlers: AutoMoveEventHandlers;
  cytoEventHandlers: CytoEventHandlers;
  createLayout(cy: CytoCore): void;
}
