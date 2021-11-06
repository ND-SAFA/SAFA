import { EventObject, NodeCollection, NodeSingular } from "cytoscape";
import { KlayLayoutSettings, LayoutHook } from "./klay";
import { AutoMoveRule } from "./automove";
import { CytoEvent, CytoEventHandlers } from "@/types";

/**
 * Fired on an auto move event.
 *
 * @param node - The node being moved.
 * @param rule - The rules for moving.
 * @param event - The event for moving.
 */
export type AutoMoveNodeEvent = (
  node: NodeSingular,
  rule: AutoMoveRule,
  event: EventObject
) => void;

/**
 * Defines an auto move event.
 */
export interface AutoMoveEventDefinition {
  /**
   * Events that trigger this auto move.
   */
  triggers: CytoEvent[];
  /**
   * The auto move action.
   */
  action: AutoMoveNodeEvent;
}

/**
 * A collection of auto move event handlers.
 */
export type AutoMoveEventHandlers = Record<string, AutoMoveEventDefinition>;

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
}
