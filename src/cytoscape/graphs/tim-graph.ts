import { CytoscapeOptions } from "cytoscape";
import {
  CytoscapeStyle,
  DEFAULT_ARTIFACT_TREE_ZOOM,
  MOTION_BLUE_OPACITY,
  artifactHtml as nodeHTML,
  nodeWarningHtml,
  timTreeResolveCy,
  USE_MOTION_BLUR,
} from "@/cytoscape";
import { CytoCoreGraph } from "@/types/cytoscape/core/cyto-core-graph";
import { viewportModule } from "@/store";
import klay from "cytoscape-klay";
import { TimStyleSheets } from "@/cytoscape/styles/stylesheets/tim-styles";
import { CytoCore } from "@/types";
import { timNodeHtml } from "@/cytoscape/styles/html/tim-html";
import nodeHtmlLabel from "cytoscape-node-html-label";

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
  afterInit: async (cy: CytoCore) => {
    await viewportModule.setTimTreeLayout();
    // cy.zoom(1);
    cy.fit(cy.nodes());
    cy.nodeHtmlLabel([timNodeHtml]);
  },
};
