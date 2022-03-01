import {
  FixedAlignment,
  LayoutDirection,
  NodeLayering,
  NodePlacement,
} from "@/types";

/**
 * Artifact node fields.
 */
export const ARTIFACT_PADDING = 50;
export const ARTIFACT_WIDTH = 105;
export const ARTIFACT_HEIGHT = (ARTIFACT_WIDTH * 9) / 16;

export const ARTIFACT_COLOR = "#888888";
export const ARTIFACT_SHAPE = "roundrectangle";

export const ARTIFACT_BORDER_STYLE = "solid";
export const ARTIFACT_BORDER_WIDTH = 0;

export const ARTIFACT_TRUNCATE_LENGTH = 150;
export const ARTIFACT_REDUCED_TRUNCATE_LENGTH = 100;

export const ARTIFACT_SELECTED_BORDER_WIDTH = 6;

/**
 * Graph specific values.
 */
export const CENTER_GRAPH_PADDING = 10;
export const DEFAULT_ARTIFACT_TREE_ZOOM = 0.75;

/**
 * Layout Options.
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
 * Custom shapes.
 */
export const POLYGON_AND =
  "-0.8 -0.4, -0.7 -0.6, -0.6 -0.75, -0.5 -0.84, -0.4 -0.9, -0.3 -0.95, -0.2 -0.98, -0.1 -0.99, 0 -1, " +
  "0.1 -0.99, 0.2 -0.98, 0.3 -0.95, 0.4 -0.9, 0.5 -0.84, 0.6 -0.75, 0.7 -0.6, 0.8 -0.4, " +
  "0.8 1, -0.8 1";

export const POLYGON_OR =
  "-0.8 0, -0.7 -0.23, -0.6 -0.43, -0.5 -0.56, -0.4 -0.68, -0.3 -0.79, -0.2 -0.87, -0.1 -0.94, 0 -1, " +
  "0.1 -0.94, 0.2 -0.87, 0.3 -0.79, 0.4 -0.68, 0.5 -0.56, 0.6 -0.43, 0.7 -0.23, 0.8 0, " +
  "0.8 1, 0.7 0.95, 0.6 0.91, 0.5 0.88, 0.4 0.85, 0.3 0.83, 0.2 0.82, 0.1 0.81, 0 0.8, " +
  "-0.1 0.81, -0.2 0.82, -0.3 0.83, -0.4 0.85, -0.5 0.88, -0.6 0.91, -0.7 0.95, -0.8 1";
