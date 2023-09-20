import { CytoscapeOptions } from "cytoscape";
import {
  DEFAULT_ARTIFACT_TREE_ZOOM,
  USE_MOTION_BLUR,
  ZOOM_INCREMENT,
} from "@/cytoscape/styles/config";
import { edgeStyles, nodeStyles } from "@/cytoscape/styles/stylesheets";

export const GRAPH_CONFIG: CytoscapeOptions = {
  style: [...nodeStyles, ...edgeStyles],
  motionBlur: USE_MOTION_BLUR,
  zoom: DEFAULT_ARTIFACT_TREE_ZOOM,
  boxSelectionEnabled: true,
  wheelSensitivity: ZOOM_INCREMENT,
};
