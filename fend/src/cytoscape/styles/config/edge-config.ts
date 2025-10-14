import { GraphMode } from "@/types";
import { ThemeColors } from "@/util";

/**
 * General edge configuration.
 */
export const EDGE_WIDTH = 3;
export const EDGE_ARROW_SCALE = 2;

export const EDGE_COLOR = {
  DEFAULT: ThemeColors.nodeDefault,
  GENERATED: ThemeColors.nodeGenerated,
  GHOST: ThemeColors.primary,
  ADDED: ThemeColors.added,
  MODIFIED: ThemeColors.modified,
  REMOVED: ThemeColors.removed,
  NO_CHANGE: ThemeColors.unchanged,
};

export const EDGE_SHAPE = {
  SOURCE: "none",
  TARGET: "chevron",
};

/**
 * Artifact edge configuration.
 */
export const TRACE_CURVE_STYLE = "bezier";
export const TRACE_FADED_OPACITY = 0.3;

export const GENERATED_TRACE_MAX_WIDTH = 6;

export const TRACE_LINE_STYLE = {
  DEFAULT: "solid",
  UNREVIEWED: "dashed",
  CREATION: "dotted",
};

/**
 * TIM edge configuration.
 */
export const TIM_EDGE_SELECTOR = `edge[graph='${"tim" as GraphMode}']`;

export const TIM_EDGE_STYLE = "taxi";
export const TIM_EDGE_ARROW_SHAPE = "chevron";
export const TIM_EDGE_X_MARGIN = 10;
export const TIM_EDGE_FONT_WEIGHT = 400;
export const TIM_EDGE_FONT_SIZE = 20;
export const TIM_EDGE_FONT_BG_OPACITY = 0.8;
export const TIM_EDGE_LOOP_STEP_SIZE = 140;
