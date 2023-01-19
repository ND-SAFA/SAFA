import { EventObject } from "cytoscape";
import {
  ArtifactCytoElementData,
  DetailsOpenState,
  GraphMode,
  TraceCytoElementData,
} from "@/types";
import { appStore, layoutStore, selectionStore, traceStore } from "@/hooks";
import { disableDrawMode } from "@/cytoscape";
import { DefaultCytoEvents } from "@/cytoscape/events/cyto-events";
import { CytoCore, CytoEvent, CytoEventHandlers } from "@/types/cytoscape/core";

/**
 * Handlers for mouse events on the artifact tree.
 */
export const ArtifactTreeCytoEvents: CytoEventHandlers = {
  ...DefaultCytoEvents,
  setInitialPosition: {
    events: [CytoEvent.ADD],
    action(cy: CytoCore, event: EventObject) {
      const artifact = event.target.data() as ArtifactCytoElementData;

      cy.nodes()
        .filter((n) => n.data().id === artifact.id)
        .layout(layoutStore.layoutOptions)
        .run();

      if (artifact.id === selectionStore.selectedArtifactId) {
        selectionStore.selectArtifact(artifact.id);
      }
    },
  },
  unselectArtifactOnBackgroundClick: {
    events: [CytoEvent.TAP],
    action(cy: CytoCore, event: EventObject) {
      if (event.target === cy) {
        disableDrawMode();

        // Don't close the side panels if an object is being edited.
        if (
          (
            ["document", "saveArtifact", "saveTrace"] as DetailsOpenState[]
          ).includes(appStore.isDetailsPanelOpen)
        )
          return;

        selectionStore.clearSelections();
      }
    },
  },
  select: {
    events: [CytoEvent.TAP],
    selector: `node[graph='${GraphMode.tree}']`,
    action(cy: CytoCore, event: EventObject) {
      const artifact = event.target.data() as ArtifactCytoElementData;

      if (!artifact.id) return;

      selectionStore.selectArtifact(artifact.id);
    },
  },
  selectAll: {
    events: [CytoEvent.BOX_SELECT],
    action(cy: CytoCore, event: EventObject) {
      const artifact = event.target.data() as ArtifactCytoElementData;

      selectionStore.addToSelectedGroup(artifact.id);
    },
  },

  selectEdge: {
    events: [CytoEvent.TAP],
    selector: `edge[graph='${GraphMode.tree}']`,
    action(cy: CytoCore, event: EventObject) {
      const data = event.target.data() as TraceCytoElementData;
      const trace = traceStore.getTraceLinkById(data.id);

      if (!trace) return;

      selectionStore.selectTraceLink(trace);
    },
  },
};
