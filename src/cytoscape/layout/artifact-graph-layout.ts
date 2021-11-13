import { ArtifactKlaySettings } from "@/cytoscape/layout/artifact-klay-settings";
import { ArtifactTreeAutoMoveHandlers } from "@/cytoscape/plugins/automove/artifact-tree-auto-move-handlers";
import { ArtifactTreeCytoEvents } from "@/cytoscape/events/artifact-tree-events";
import { DefaultPreLayoutHooks } from "@/cytoscape/hooks/pre-layout";
import { DefaultPostLayoutHooks } from "@/cytoscape/hooks/post-layout";
import GraphLayout from "./graph-layout";

export default class ArtifactGraphLayout extends GraphLayout {
  constructor() {
    super(
      ArtifactTreeAutoMoveHandlers,
      ArtifactTreeCytoEvents,
      ArtifactKlaySettings,
      DefaultPreLayoutHooks,
      DefaultPostLayoutHooks
    );
  }
}
