import { CollectionReturnValue, EventObject, NodeSingular } from "cytoscape";

import { ArtifactData, CytoCore } from "@/types";
import { handleCreateLink } from "@/api";
import { disableDrawMode } from "@/cytoscape";

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
  const sourceData: ArtifactData = sourceNode.data();
  const targetData: ArtifactData = targetNode.data();

  disableDrawMode();

  addedEdge.remove();

  handleCreateLink(sourceData, targetData);
}
