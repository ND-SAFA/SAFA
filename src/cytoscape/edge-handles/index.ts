import { CytoCore, CytoEvent, EdgeHandleCore } from "@/types/cytoscape";
import { NodeSingular, CollectionReturnValue } from "cytoscape";
import { onArtifactTreeEdgeComplete } from "@/cytoscape/edge-handles/onComplete";

export * from "./options";

let edgeHandlesCore: EdgeHandleCore | undefined = undefined;

export function setEdgeHandlesCore(
  cyPromise: Promise<CytoCore>,
  instance: EdgeHandleCore
): Promise<void> {
  edgeHandlesCore = instance;
  return cyPromise.then((cytoCore: CytoCore) => {
    cytoCore.on(CytoEvent.EH_COMPLETE, (event, ...args: unknown[]) =>
      onArtifactTreeEdgeComplete(
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
