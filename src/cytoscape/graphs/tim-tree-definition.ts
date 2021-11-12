import { CytoscapeOptions } from "cytoscape";
import {
  CytoscapeStyle,
  DEFAULT_ZOOM,
  MOTION_BLUE_OPACITY,
  USE_MOTION_BLUR,
} from "@/cytoscape";
import { CytoCoreGraph } from "@/types/cytoscape/core/cyto-core-graph";
import { timTreeResolveCy } from "./tim-tree-cy";

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
  afterInit: () => undefined,
};
