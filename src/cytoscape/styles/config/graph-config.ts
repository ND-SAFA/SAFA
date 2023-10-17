import {
  FixedAlignment,
  LayoutDirection,
  NodeLayering,
  NodePlacement,
} from "@/types";

/**
 * General configuration.
 */
export const USE_MOTION_BLUR = false;
export const ANIMATION_DURATION = 300; // ms

/**
 * Viewport configuration.
 */
export const DEFAULT_ARTIFACT_TREE_ZOOM = 0.75;
export const ZOOM_INCREMENT = 0.05;

export const CENTER_GRAPH_PADDING = 100;

/**
 * TIM Layout configuration.
 */
export const LAYOUT_NODE_DIRECTION = LayoutDirection.DOWN;
export const LAYOUT_ALIGNMENT = FixedAlignment.BALANCED;
export const LAYOUT_USE_HIERARCHY = true;
export const LAYOUT_NODE_LAYERING = NodeLayering.NETWORK_SIMPLEX;
export const LAYOUT_NODE_PLACEMENT = NodePlacement.BRANDES_KOEPF;
export const LAYOUT_THOROUGHNESS = 10;
export const LAYOUT_RANDOM_SEED = 42;
export const LAYOUT_NODE_SPACING = 50;
