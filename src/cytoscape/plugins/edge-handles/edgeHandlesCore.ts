import { CytoCore, CytoEvent, EdgeHandleCore } from "@/types";
import { onArtifactTreeEdgeComplete } from "@/cytoscape/plugins/edge-handles/onComplete";
import { CollectionReturnValue, NodeSingular } from "cytoscape";

let edgeHandlesCore: EdgeHandleCore | undefined = undefined;

export function setEdgeHandlesCore(
  cyPromise: Promise<CytoCore>,
  instance: EdgeHandleCore
): Promise<void> {
  edgeHandlesCore = instance;
  return cyPromise.then((cytoCore: CytoCore) => {
    cytoCore.on(CytoEvent.EH_COMPLETE, (event, ...args: unknown[]) =>
      onArtifactTreeEdgeComplete(
        cytoCore,
        event,
        args[0] as NodeSingular,
        args[1] as NodeSingular,
        args[2] as CollectionReturnValue
      )
    );
  });
}

export function getEdgeHandlesCore(): EdgeHandleCore {
  if (edgeHandlesCore === undefined) {
    throw Error("EdgeHandles has not been instantiated");
  }
  return edgeHandlesCore;
}

export function enableDrawMode(): void {
  getEdgeHandlesCore().enable();
  getEdgeHandlesCore().enableDrawMode();
}

export function disableDrawMode(): void {
  getEdgeHandlesCore().disableDrawMode();
  getEdgeHandlesCore().disable();
}
