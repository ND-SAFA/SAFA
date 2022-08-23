import { CytoCore, CytoEvent, EdgeHandleCore } from "@/types";
import { onArtifactTreeEdgeComplete } from "@/cytoscape/plugins/edge-handles/on-complete";
import { CollectionReturnValue, NodeSingular } from "cytoscape";
import { appStore, logStore } from "@/hooks";

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
 * Returns the edge handle core.
 */
export function getEdgeHandlesCore(): EdgeHandleCore | undefined {
  if (edgeHandlesCore === undefined) {
    logStore.onDevError("EdgeHandles has not been instantiated");
  }

  return edgeHandlesCore;
}

/**
 * Enables edge drawing mode.
 */
export function enableDrawMode(): void {
  const core = getEdgeHandlesCore();

  if (!core) return;

  core.enable();
  core.enableDrawMode();
  appStore.enableDrawLink();
}

/**
 * Disables edge drawing mode.
 */
export function disableDrawMode(): void {
  const core = getEdgeHandlesCore();

  if (!core) return;

  core.disableDrawMode();
  core.disable();
  appStore.disableDrawLink();
}
