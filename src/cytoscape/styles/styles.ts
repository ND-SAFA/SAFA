import { CytoscapeOptions } from "cytoscape";
import { KlayLayoutSettings } from "@/types";
import {
  DEFAULT_ARTIFACT_TREE_ZOOM,
  LAYOUT_ALIGNMENT,
  LAYOUT_NODE_DIRECTION,
  LAYOUT_NODE_LAYERING,
  LAYOUT_NODE_PLACEMENT,
  LAYOUT_NODE_SPACING,
  LAYOUT_RANDOM_SEED,
  LAYOUT_THOROUGHNESS,
  LAYOUT_USE_HIERARCHY,
  USE_MOTION_BLUR,
  ZOOM_INCREMENT,
} from "@/cytoscape/styles/config";
import { edgeStyles, nodeStyles } from "@/cytoscape/styles/stylesheets";

/**
 * Settings for generating the graph layout.
 */
export const KLAY_CONFIG: KlayLayoutSettings = {
  spacing: LAYOUT_NODE_SPACING,
  direction: LAYOUT_NODE_DIRECTION,
  fixedAlignment: LAYOUT_ALIGNMENT,
  layoutHierarchy: LAYOUT_USE_HIERARCHY,
  nodeLayering: LAYOUT_NODE_LAYERING,
  nodePlacement: LAYOUT_NODE_PLACEMENT,
  thoroughness: LAYOUT_THOROUGHNESS,
  randomizationSeed: LAYOUT_RANDOM_SEED,
};

/**
 * The configuration for the graph.
 */
export const GRAPH_CONFIG: CytoscapeOptions = {
  style: [...nodeStyles, ...edgeStyles],
  motionBlur: USE_MOTION_BLUR,
  zoom: DEFAULT_ARTIFACT_TREE_ZOOM,
  boxSelectionEnabled: true,
  wheelSensitivity: ZOOM_INCREMENT,
};
