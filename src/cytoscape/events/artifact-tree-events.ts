import { CytoCore, CytoEvent, CytoEventHandlers } from "@/types/cytoscape/core";
import { artifactSelectionModule } from "@/store";
import { EventObject } from "cytoscape";
import { DefaultCytoEvents } from "@/cytoscape/events/cyto-events";

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
};
