import { CytoscapeOptions } from "cytoscape";
import {
  CytoscapeStyle,
  DEFAULT_ZOOM,
  MOTION_BLUE_OPACITY,
  TimGraphLayout,
  timTreeResolveCy,
  USE_MOTION_BLUR,
} from "@/cytoscape";
import { CytoCoreGraph } from "@/types/cytoscape/core/cyto-core-graph";
import { viewportModule } from "@/store";
import { CytoCore, IGraphLayout } from "@/types";
import ArtifactGraphLayout from "../layout/artifact-graph-layout";

const timTreeConfig: CytoscapeOptions = {
  style: CytoscapeStyle,
  motionBlur: USE_MOTION_BLUR,
  motionBlurOpacity: MOTION_BLUE_OPACITY,
  zoom: DEFAULT_ZOOM,
};

export const timTreeDefinition: CytoCoreGraph = {
  name: "tim-tree-graph",
  config: timTreeConfig,
  saveCy: timTreeResolveCy,
  plugins: [],
  afterInit: async (cy: CytoCore) => {
    const cyPromise: Promise<CytoCore> = new Promise((resolve) => resolve(cy));
    const layout = new TimGraphLayout();
    await viewportModule.setGraphLayout(cyPromise, layout as IGraphLayout);
  },
};
