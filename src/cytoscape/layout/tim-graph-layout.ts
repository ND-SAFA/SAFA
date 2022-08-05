import { DefaultCytoEvents } from "@/cytoscape/events";
import { TimKlaySettings } from "./tim-klay-settings";
import GraphLayout from "./graph-layout";
import { TIMPostLayoutHooks, TIMPreLayoutHooks } from "@/cytoscape";

/**
 * Defines the layout of the tim graph.
 */
export default class TimGraphLayout extends GraphLayout {
  constructor() {
    super(
      {},
      DefaultCytoEvents,
      TimKlaySettings,
      TIMPreLayoutHooks,
      TIMPostLayoutHooks
    );
  }
}
