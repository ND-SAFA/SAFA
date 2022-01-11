import klay from "cytoscape-klay";
import nodeHtmlLabel from "cytoscape-node-html-label";
import { CytoCoreGraph, CytoCore } from "@/types";
import { viewportModule } from "@/store";
import {
  DEFAULT_ARTIFACT_TREE_ZOOM,
  MOTION_BLUE_OPACITY,
  USE_MOTION_BLUR,
} from "@/cytoscape";
import { timTreeResolveCy } from "@/cytoscape/cy";
import { TimStyleSheets } from "@/cytoscape/styles/stylesheets/tim-styles";
import { timNodeHtml } from "@/cytoscape/styles/html/tim-html";

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
      afterInit: (cy: CytoCore) => cy.nodeHtmlLabel([timNodeHtml]),
    },
  ],
  afterInit: async () => {
    await viewportModule.setTimTreeLayout();
  },
};
