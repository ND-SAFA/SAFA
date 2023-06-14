import { EventObject } from "cytoscape";
import {
  ArtifactCytoElementData,
  DetailsOpenState,
  TimEdgeCytoElementData,
  TimNodeCytoElementData,
  TraceCytoElementData,
} from "@/types";
import {
  appStore,
  documentStore,
  layoutStore,
  selectionStore,
  traceStore,
} from "@/hooks";
import {
  ARTIFACT_EDGE_SELECTOR,
  ARTIFACT_NODE_SELECTOR,
  TIM_EDGE_SELECTOR,
  TIM_NODE_SELECTOR,
} from "@/cytoscape/styles";
import { disableDrawMode } from "@/cytoscape/plugins";
import { DefaultCytoEvents } from "@/cytoscape/events/cyto-events";
import { CytoCore, CytoEvent, CytoEventHandlers } from "@/types/cytoscape/core";

/**
 * Handlers for mouse events on the artifact tree.
 */
export const ArtifactTreeCytoEvents: CytoEventHandlers = {
  ...DefaultCytoEvents,
  setInitialArtifactPosition: {
    events: [CytoEvent.ADD],
    selector: ARTIFACT_NODE_SELECTOR,
    action(cy: CytoCore, event: EventObject) {
      const artifact = event.target.data() as ArtifactCytoElementData;

      cy.getElementById(artifact.id).layout(layoutStore.layoutOptions).run();

      if (artifact.id === selectionStore.selectedArtifact?.id) {
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

        selectionStore.clearSelections(true);
      }
    },
  },
  selectArtifact: {
    events: [CytoEvent.TAP],
    selector: ARTIFACT_NODE_SELECTOR,
    action(cy: CytoCore, event: EventObject) {
      const artifact = event.target.data() as ArtifactCytoElementData;

      if (!artifact.id) return;

      selectionStore.selectArtifact(artifact.id);
    },
  },
  selectAllArtifacts: {
    events: [CytoEvent.BOX_SELECT],
    action(cy: CytoCore, event: EventObject) {
      const artifact = event.target.data() as ArtifactCytoElementData;

      selectionStore.addToSelectedGroup(artifact.id);
    },
  },
  selectTraceLink: {
    events: [CytoEvent.TAP],
    selector: ARTIFACT_EDGE_SELECTOR,
    action(cy: CytoCore, event: EventObject) {
      const data = event.target.data() as TraceCytoElementData;
      const trace = traceStore.getTraceLinkById(data.id);

      if (!trace) return;

      selectionStore.selectTraceLink(trace);
    },
  },
  selectTimNode: {
    events: [CytoEvent.TAP],
    selector: TIM_NODE_SELECTOR,
    action(cy: CytoCore, event: EventObject) {
      const artifactLevel = event.target.data() as TimNodeCytoElementData;

      if (!artifactLevel.artifactType) return;

      if (
        selectionStore.selectedArtifactLevelType !== artifactLevel.artifactType
      ) {
        selectionStore.selectArtifactLevel(artifactLevel.artifactType);
      } else {
        documentStore.addDocumentOfTypes([artifactLevel.artifactType]);
      }
    },
  },
  selectTimEdge: {
    events: [CytoEvent.TAP],
    selector: TIM_EDGE_SELECTOR,
    action(cy: CytoCore, event: EventObject) {
      const artifactLevel = event.target.data() as TimEdgeCytoElementData;

      if (!artifactLevel.source || !artifactLevel.target) return;

      if (
        selectionStore.selectedTraceMatrixTypes[0] !== artifactLevel.target ||
        selectionStore.selectedTraceMatrixTypes[1] !== artifactLevel.source
      ) {
        selectionStore.selectTraceMatrix(
          artifactLevel.target,
          artifactLevel.source
        );
      } else {
        documentStore.addDocumentOfTypes([
          artifactLevel.targetType,
          artifactLevel.sourceType,
        ]);
      }
    },
  },
};
