import klay from "cytoscape-klay";
import nodeHtmlLabel from "cytoscape-node-html-label";

import { CytoCoreGraph } from "@/types";
import { layoutStore } from "@/hooks";
import { timTreeResolveCy } from "@/cytoscape/cy";
import {
  DEFAULT_ARTIFACT_TREE_ZOOM,
  USE_MOTION_BLUR,
  nodeStyles,
  edgeStyles,
} from "@/cytoscape/styles";

/**
 * Defines the initialization of the tim graph.
 */
export const timGraph: CytoCoreGraph = {
  name: "tim-tree-graph",
  config: {
    style: [...nodeStyles, ...edgeStyles],
    motionBlur: USE_MOTION_BLUR,
    zoom: DEFAULT_ARTIFACT_TREE_ZOOM,
  },
  saveCy: timTreeResolveCy,
  plugins: [
    {
      initialize: klay,
      afterInit: () => undefined,
    },
    {
      initialize: nodeHtmlLabel,
      afterInit: () => undefined,
    },
  ],
  async afterInit() {
    await layoutStore.setTimTreeLayout();
  },
};
