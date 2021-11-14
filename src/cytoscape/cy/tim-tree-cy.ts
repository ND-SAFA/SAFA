import { CyPromise, ResolveCy } from "@/types";

export let timTreeResolveCy: ResolveCy = null;

export const timTreeCyPromise: CyPromise = new Promise(
  (resolve) => (timTreeResolveCy = resolve)
);
