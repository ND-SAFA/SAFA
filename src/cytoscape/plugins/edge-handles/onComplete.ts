import { NodeSingular, EventObject, CollectionReturnValue } from "cytoscape";
import { appModule, projectModule } from "@/store";
import { createLink } from "@/api";
import { disableDrawMode } from "@/cytoscape/plugins/edge-handles/index";

export function onArtifactTreeEdgeComplete(
  event: EventObject,
  sourceNode: NodeSingular,
  targetNode: NodeSingular,
  addedEdge: CollectionReturnValue
): void {
  disableDrawMode();
  const versionId = getVersionId(() => addedEdge.remove());
  const sourceId = sourceNode.data().id;
  const targetId = targetNode.data().id;

  createLink(versionId, sourceId, targetId)
    .then(() => {
      addedEdge.remove();
    })
    .catch((e) => console.error(e));
}
function getVersionId(beforeError: () => void): string {
  const versionId = projectModule.getProject.projectVersion?.versionId;
  if (versionId === undefined) {
    const errorMessage =
      "Please select a project version before creating trace links";
    appModule.onWarning(errorMessage);
    beforeError();
    throw Error(errorMessage);
  }
  return versionId;
}
