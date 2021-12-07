import { CollectionReturnValue, EventObject, NodeSingular } from "cytoscape";
import { createLink } from "@/api";
import { disableDrawMode } from "@/cytoscape/plugins/edge-handles/index";
import { TraceApproval, TraceLink, TraceType } from "@/types";

/**
 * Creates the finalized trace link when an edge creation draw is completed.
 *
 * @param event - The creation event.
 * @param sourceNode - The target node, being the one dragged from.
 * @param targetNode - The source node, being the one dragged to.
 * @param addedEdge - The temporary edge that was added.
 */
export function onArtifactTreeEdgeComplete(
  event: EventObject,
  sourceNode: NodeSingular,
  targetNode: NodeSingular,
  addedEdge: CollectionReturnValue
): void {
  const sourceId = sourceNode.data().id;
  const targetId = targetNode.data().id;
  const traceLink: TraceLink = {
    traceLinkId: "",
    source: sourceId,
    target: targetId,
    traceType: TraceType.MANUAL,
    approvalStatus: TraceApproval.APPROVED,
    score: 1,
  };

  disableDrawMode();

  createLink(traceLink)
    .then(() => {
      addedEdge.remove();
    })
    .catch((e) => console.error(e));
}
