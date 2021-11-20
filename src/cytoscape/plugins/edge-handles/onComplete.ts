import { CollectionReturnValue, EventObject, NodeSingular } from "cytoscape";
import { createLink } from "@/api";
import { disableDrawMode } from "@/cytoscape/plugins/edge-handles/index";
import { TraceApproval, TraceLink, TraceType } from "@/types";

export function onArtifactTreeEdgeComplete(
  event: EventObject,
  sourceNode: NodeSingular,
  targetNode: NodeSingular,
  addedEdge: CollectionReturnValue
): void {
  disableDrawMode();
  const sourceId = sourceNode.data().id;
  const targetId = targetNode.data().id;
  const traceLink: TraceLink = {
    source: sourceId,
    target: targetId,
    approvalStatus: TraceApproval.APPROVED,
    traceLinkId: "",
    score: 1,
    traceType: TraceType.MANUAL,
  };

  createLink(traceLink)
    .then(() => {
      addedEdge.remove();
    })
    .catch((e) => console.error(e));
}
