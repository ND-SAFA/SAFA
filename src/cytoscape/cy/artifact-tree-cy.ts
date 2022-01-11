import { CyPromise, ResolveCy } from "@/types";

export let artifactTreeResolveCy: ResolveCy = null;

/**
 * Returns a promise for the artifact tree cy instance.
 * This promise will only resolve when there is a cytoscape graph.
 */
export const artifactTreeCyPromise: CyPromise = new Promise(
  (resolve) => (artifactTreeResolveCy = resolve)
);
