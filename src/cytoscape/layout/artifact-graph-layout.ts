import { ArtifactTreeAutoMoveHandlers } from "@/cytoscape/plugins";
import { ArtifactTreeCytoEvents } from "@/cytoscape/events";
import {
  DefaultPreLayoutHooks,
  DefaultPostLayoutHooks,
} from "@/cytoscape/hooks";
import GraphLayout from "./graph-layout";

/**
 * Defines the layout of the artifact graph.
 */
export default class ArtifactGraphLayout extends GraphLayout {
  constructor() {
    super(
      ArtifactTreeAutoMoveHandlers,
      ArtifactTreeCytoEvents,
      undefined,
      DefaultPreLayoutHooks,
      DefaultPostLayoutHooks
    );
  }
}
