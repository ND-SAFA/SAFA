import { CytoscapeOptions } from "cytoscape";
import {
  CytoscapeStyle,
  DEFAULT_ZOOM,
  MOTION_BLUE_OPACITY,
  TimGraphLayout,
  timTreeCyPromise,
  timTreeResolveCy,
  USE_MOTION_BLUR,
} from "@/cytoscape";
import { CytoCoreGraph } from "@/types/cytoscape/core/cyto-core-graph";
import { viewportModule } from "@/store";
import klay from "cytoscape-klay";
import { ViewportModule } from "@/store/modules";

const timTreeConfig: CytoscapeOptions = {
  style: CytoscapeStyle,
  motionBlur: USE_MOTION_BLUR,
  motionBlurOpacity: MOTION_BLUE_OPACITY,
  zoom: DEFAULT_ZOOM,
};

export const timGraph: CytoCoreGraph = {
  name: "tim-tree-graph",
  config: timTreeConfig,
  saveCy: timTreeResolveCy,
  plugins: [
    {
      initialize: klay,
      afterInit: () => undefined,
    },
  ],
  afterInit: async () => {
    const layout = new TimGraphLayout();
    await ViewportModule.setGraphLayout(timTreeCyPromise, layout, undefined);
  },
};
