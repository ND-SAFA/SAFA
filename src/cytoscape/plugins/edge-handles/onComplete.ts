import { CollectionReturnValue, EventObject, NodeSingular } from "cytoscape";
import { createLink } from "@/api";
import { disableDrawMode } from "@/cytoscape/plugins/edge-handles/index";
import { TraceApproval, TraceLink, TraceType } from "@/types";

export function onArtifactTreeEdgeComplete(
  event: EventObject,
  targetNode: NodeSingular,
  sourceNode: NodeSingular,
  addedEdge: CollectionReturnValue
): void {
  disableDrawMode();
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

  createLink(traceLink)
    .then(() => {
      addedEdge.remove();
    })
    .catch((e) => console.error(e));
}
