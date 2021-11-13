import {
  DEFAULT_ARTIFACT_TREE_ZOOM,
  MOTION_BLUE_OPACITY,
  timTreeResolveCy,
  USE_MOTION_BLUR,
  TimGraphLayout,
  timTreeCyPromise,
  ANIMATION_DURATION,
} from "@/cytoscape";
import { CytoCoreGraph } from "@/types/cytoscape/core/cyto-core-graph";
import { appModule, viewportModule } from "@/store";
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
    const layout = new TimGraphLayout();
    const payload = { layout, cyPromise: timTreeCyPromise };
    //TODO: Figure out why I can't immediately call animate function
    //after setting graph layout
    appModule.SET_IS_LOADING(true);
    await viewportModule.setGraphLayout(payload);
    cy.nodeHtmlLabel([timNodeHtml]);
    setTimeout(() => {
      cy.animate({
        center: { eles: cy.nodes() },
        duration: ANIMATION_DURATION,
        complete: () => appModule.SET_IS_LOADING(false),
      });
    }, 250);
  },
};
