import { CollectionReturnValue, NodeSingular } from "cytoscape";
import { CytoCore, CytoEvent, EdgeHandleCore } from "@/types";
import { appStore } from "@/hooks";
import { onArtifactTreeEdgeComplete } from "./on-complete";

let edgeHandlesCore: EdgeHandleCore | undefined = undefined;

/**
 * Initializes edge handling.
 *
 * @param cyPromise - The cy instance.
 * @param instance - The edge handles instance.
 */
export function setEdgeHandlesCore(
  cyPromise: Promise<CytoCore>,
  instance: EdgeHandleCore
): Promise<void> {
  edgeHandlesCore = instance;

  return cyPromise.then((cy: CytoCore) => {
    cy.on(CytoEvent.EH_COMPLETE, (event, ...args: unknown[]) =>
      onArtifactTreeEdgeComplete(
        cy,
        event,
        args[0] as NodeSingular,
        args[1] as NodeSingular,
        args[2] as CollectionReturnValue
      )
    );
  });
}

/**
 * Enables edge drawing mode.
 */
export function enableDrawMode(): void {
  if (!edgeHandlesCore) return;

  edgeHandlesCore.enable();
  edgeHandlesCore.enableDrawMode();
  appStore.enableDrawLink();
}

/**
 * Disables edge drawing mode.
 */
export function disableDrawMode(): void {
  if (!edgeHandlesCore) return;

  edgeHandlesCore.disableDrawMode();
  edgeHandlesCore.disable();
  appStore.disableDrawLink();
}
