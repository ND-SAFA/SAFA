import {
  FixedAlignment,
  LayoutDirection,
  NodeLayering,
  NodePlacement,
} from "@/types";
import { GraphStyle } from "@/cytoscape/styles/stylesheets";
import { CytoscapeOptions } from "cytoscape";

export const EDGE_CURVE_STYLE = "bezier";
export const CORE_PEER_SPACING = 1;

/**
 * Layout Options
 */
export const LAYOUT_NODE_SPACING = 20;
export const LAYOUT_NODE_DIRECTION = LayoutDirection.DOWN;
export const LAYOUT_ALIGNMENT = FixedAlignment.BALANCED;
export const LAYOUT_USE_HIERARCHY = true;
export const LAYOUT_NODE_LAYERING = NodeLayering.NETWORK_SIMPLEX;
export const LAYOUT_NODE_PLACEMENT = NodePlacement.BRANDES_KOEPF;
export const LAYOUT_NODE_INNER_SPACING = 0.4; // Factor by which the usual spacing is multiplied to determine the in-layer spacing between objects.
export const LAYOUT_THOROUGHNESS = 10; // How much effort should be spent to produce a nice layout..
export const LAYOUT_RANDOM_SEED = 42;
/**
 * Cytoscape Options
 */
export const USE_MOTION_BLUR = false;
export const MOTION_BLUE_OPACITY = 0.2;
export const ZOOM_INCREMENT = 0.05;

export const DEFAULT_ZOOM = 0.75;
export const DEFAULT_PAN = 1;
export const ANIMATION_DURATION = 250; // ms
export const CENTER_GRAPH_PADDING = 10;
export const TRUNCATE_LENGTH = 75;
export const GRAPH_CONFIG: CytoscapeOptions = {
  style: GraphStyle,
  motionBlur: USE_MOTION_BLUR,
  motionBlurOpacity: MOTION_BLUE_OPACITY,
  zoom: DEFAULT_ZOOM,
};
