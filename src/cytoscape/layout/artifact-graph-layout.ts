import { ArtifactTreeAutoMoveHandlers } from "@/cytoscape/plugins";
import { ArtifactTreeCytoEvents } from "@/cytoscape/events";
import {
  DefaultPreLayoutHooks,
  DefaultPostLayoutHooks,
} from "@/cytoscape/hooks";
import GraphLayout from "./graph-layout";
import { TimKlaySettings } from "./tim-klay-settings";

/**
 * Defines the layout of the artifact graph.
 */
export default class ArtifactGraphLayout extends GraphLayout {
  constructor() {
    super(
      ArtifactTreeAutoMoveHandlers,
      ArtifactTreeCytoEvents,
      TimKlaySettings,
      DefaultPreLayoutHooks,
      DefaultPostLayoutHooks
    );
  }
}
