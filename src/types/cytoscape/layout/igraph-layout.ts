import { NodeCollection } from "cytoscape";
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
  klaySettings: KlayLayoutSettings;
  preLayoutHooks: LayoutHook[];
  postLayoutHooks: LayoutHook[];
  autoMoveHandlers: AutoMoveEventHandlers;
  cytoEventHandlers: CytoEventHandlers;
  peerNodes?: NodeCollection;
  temporaryEdges?: NodeCollection;
  packageNodes?: NodeCollection;
  ancestorNodes?: NodeCollection;
  codeNodes?: NodeCollection;
  codeElements?: NodeCollection;
  peerElements?: NodeCollection;
  createLayout(cy: CytoCore): void;
}
