import { CytoCore, CytoEvent, EdgeHandleCore } from "@/types";
import { artifactTreeCyPromise } from "@/cytoscape/cytoscape";
import { NodeSingular, CollectionReturnValue } from "cytoscape";
import { onEdgeComplete } from "@/cytoscape/edge-handles/onComplete";

export * from "./options";

let edgeHandlesCore: EdgeHandleCore | undefined = undefined;

export function setEdgeHandlesCore(instance: EdgeHandleCore): Promise<void> {
  edgeHandlesCore = instance;
  return artifactTreeCyPromise.then((cytoCore: CytoCore) => {
    cytoCore.on(CytoEvent.EH_COMPLETE, (event, ...args: unknown[]) =>
      onEdgeComplete(
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
  const core = getEdgeHandlesCore();
  core.enable();
  core.enableDrawMode();
}

export function disableDrawMode(): void {
  getEdgeHandlesCore().disableDrawMode();
  getEdgeHandlesCore().disable();
}
