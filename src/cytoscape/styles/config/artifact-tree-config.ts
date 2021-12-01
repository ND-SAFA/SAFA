import { ThemeColors } from "@/util";
import {
  FixedAlignment,
  LayoutDirection,
  NodeLayering,
  NodePlacement,
} from "@/types";

/**
 * Artifact node
 */
export const ARTIFACT_PADDING = 50;
export const ARTIFACT_WIDTH = 105;
export const ARTIFACT_HEIGHT = (ARTIFACT_WIDTH * 9) / 16;

export const ARTIFACT_SHAPE = "rectangle";
export const ARTIFACT_BORDER_STYLE = "solid";
export const ARTIFACT_BORDER_WIDTH = 1.5;

export const ARTIFACT_BACKGROUND_COLOR = ThemeColors.artifactDefault;
export const ARTIFACT_SELECTED_COLOR = ThemeColors.primary;
export const ARTIFACT_SELECTED_BORDER_WIDTH = 6;

/**
 * Delta State.
 */
export const ARTIFACT_ADDED_COLOR = ThemeColors.artifactAdded;
export const ARTIFACT_REMOVED_COLOR = ThemeColors.artifactRemoved;
export const ARTIFACT_MODIFIED_COLOR = ThemeColors.artifactModified;

/**
 * Graph specific values
 */
export const CENTER_GRAPH_PADDING = 10;
export const DEFAULT_ARTIFACT_TREE_ZOOM = 0.75;

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
