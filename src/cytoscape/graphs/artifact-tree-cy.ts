import { CyPromise, ResolveCy } from "@/types";

export let artifactTreeResolveCy: ResolveCy = null;

export const artifactTreeCyPromise: CyPromise = new Promise(
  (resolve) => (artifactTreeResolveCy = resolve)
);
