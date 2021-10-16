import { NodeCollection } from "cytoscape";
import { AutoMoveEventHandlers } from "@/cytoscape/automove";
import { CytoEventHandlers } from "@/cytoscape/events/cyto-events";
import { KlayLayoutSettings, LayoutHook } from "@/types/cytoscape/klay";

export default interface IGraphLayout {
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
}
