import { CyPromise, ResolveCy } from "@/types";

export let timTreeResolveCy: ResolveCy = null;

/**
 * Returns a promise for the tim tree cy instance.
 * This promise will only resolve when there is a cytoscape graph.
 */
export const timTreeCyPromise: CyPromise = new Promise(
  (resolve) => (timTreeResolveCy = resolve)
);
