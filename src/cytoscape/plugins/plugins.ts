import klay from "cytoscape-klay";

export const CREATOR_PLUGINS = [
  {
    initialize: klay,
    afterInit: () => undefined,
  },
];
