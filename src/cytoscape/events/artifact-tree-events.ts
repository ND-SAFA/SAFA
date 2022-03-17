import { CytoCore, CytoEvent, CytoEventHandlers } from "@/types/cytoscape/core";
import { artifactSelectionModule } from "@/store";
import { EventObject } from "cytoscape";
import { DefaultCytoEvents } from "@/cytoscape/events/cyto-events";
import { Artifact } from "@/types";

/**
 * Handlers for mouse events on the artifact tree.
 */
export const ArtifactTreeCytoEvents: CytoEventHandlers = {
  ...DefaultCytoEvents,
  unselectArtifactOnBackgroundClick: {
    events: [CytoEvent.TAP],
    action: (cy: CytoCore, event: EventObject) => {
      if (event.target === cy) {
        artifactSelectionModule.clearSelections();
      }
    },
  },
  selectAll: {
    events: [CytoEvent.BOX_SELECT],
    action: (cy: CytoCore, event: EventObject) => {
      const artifact = event.target.data() as Artifact;

      artifactSelectionModule.addToSelectedGroup(artifact.id);
    },
  },
};
