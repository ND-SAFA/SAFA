import { CollectionReturnValue, EventObject, NodeSingular } from "cytoscape";

import {
  ArtifactCytoElementData,
  CytoCore,
  TimNodeCytoElementData,
} from "@/types";
import { traceApiStore, traceMatrixApiStore } from "@/hooks";
import { disableDrawMode } from "@/cytoscape/plugins";

/**
 * Creates the finalized trace link when an edge creation draw is completed.
 *
 * @param cy - The cytoscape instance.
 * @param event - The creation event.
 * @param sourceNode - The target node, being the one dragged from.
 * @param targetNode - The source node, being the one dragged to.
 * @param addedEdge - The temporary edge that was added.
 */
export function onArtifactTreeEdgeComplete(
  cy: CytoCore,
  event: EventObject,
  sourceNode: NodeSingular,
  targetNode: NodeSingular,
  addedEdge: CollectionReturnValue
): void {
  disableDrawMode();

  addedEdge.remove();

  if (sourceNode.data()?.graph === "tree") {
    const sourceData: ArtifactCytoElementData = sourceNode.data();
    const targetData: ArtifactCytoElementData = targetNode.data();

    traceApiStore.handleCreate(sourceData, targetData);
  } else {
    const sourceData: TimNodeCytoElementData = sourceNode.data();
    const targetData: TimNodeCytoElementData = targetNode.data();

    traceMatrixApiStore.handleCreate(
      sourceData.artifactType,
      targetData.artifactType
    );
  }
}
