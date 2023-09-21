import klay from "cytoscape-klay";
import automove from "cytoscape-automove";
import edgehandles from "cytoscape-edgehandles";

/**
 * Plugins used on the creator graph.
 */
export const CREATOR_PLUGINS = [
  {
    initialize: klay,
    afterInit: () => undefined,
  },
];

/**
 * Plugins used on the project graph.
 */
export const PROJECT_PLUGINS = [
  {
    initialize: klay,
    afterInit: () => undefined,
  },
  {
    initialize: automove,
    afterInit: () => undefined,
  },
  {
    initialize: edgehandles,
    afterInit: () => undefined,
  },
];
