import { NodeCollection } from "cytoscape";
import { KlayLayoutSettings, LayoutHook } from "../plugins/klay";
import { AutoMoveEventHandlers } from "@/types";
import { CytoCore, CytoEventHandlers } from "@/types";

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
