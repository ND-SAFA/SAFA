import klay from "cytoscape-klay";
import nodeHtmlLabel from "cytoscape-node-html-label";

import { CytoCoreGraph } from "@/types";
import { layoutStore } from "@/hooks";
import { timTreeResolveCy } from "@/cytoscape/cy";
import {
  DEFAULT_ARTIFACT_TREE_ZOOM,
  MOTION_BLUE_OPACITY,
  USE_MOTION_BLUR,
  TimStyleSheets,
} from "@/cytoscape/styles";

/**
 * Defines the initialization of the tim graph.
 */
export const timGraph: CytoCoreGraph = {
  name: "tim-tree-graph",
  config: {
    style: TimStyleSheets,
    motionBlur: USE_MOTION_BLUR,
    motionBlurOpacity: MOTION_BLUE_OPACITY,
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
