import { ApprovalType, GraphMode, NodePlacement, TraceType } from "@/types";
import { ThemeColors } from "@/util";

/**
 * General node configuration.
 */
export const NODE_BORDER_WIDTH = 0;

export const NODE_BORDER_COLOR = ThemeColors.nodeDefault;
export const NODE_BG_COLOR = {
  LIGHT: ThemeColors.whiteBg,
  DARK: ThemeColors.blackBg,
};

/**
 * Artifact node configuration.
 */
export const ARTIFACT_NODE_SELECTOR = `node[graph='${"tree" as GraphMode}']`;
export const ARTIFACT_EDGE_SELECTOR = `edge[graph='${"tree" as GraphMode}']`;
export const GENERATED_LINK_SELECTOR = `${ARTIFACT_EDGE_SELECTOR}[traceType='${
  "GENERATED" as TraceType
}']`;
export const GENERATED_APPROVED_LINK_SELECTOR = `${GENERATED_LINK_SELECTOR}[approvalStatus='${
  "APPROVED" as ApprovalType
}']`;

export const ARTIFACT_WIDTH = 105;
export const ARTIFACT_HEIGHT = (ARTIFACT_WIDTH * 9) / 16;
export const ARTIFACT_PADDING = 50;
export const ARTIFACT_BORDER_STYLE = "solid";
export const ARTIFACT_FTA_BORDER_WIDTH = 2;

export const ARTIFACT_SHAPE = {
  DEFAULT: NodePlacement.ROUND_RECTANGLE,
  FTA: NodePlacement.POLYGON,
  SC_GOAL: NodePlacement.RECTANGLE,
  SC_CONTEXT: NodePlacement.ROUND_RECTANGLE,
  SC_SOLUTION: NodePlacement.ELLIPSE,
  SC_STRATEGY: NodePlacement.POLYGON,
};

export const ARTIFACT_POLYGONS = {
  FTA_AND:
    "-0.4 -0.2, -0.35 -0.3, -0.3 -0.375, -0.25 -0.42, -0.2 -0.45, -0.15 -0.475, -0.1 -0.49, -0.05 -0.495, 0 -0.5, " +
    "0.05 -0.495, 0.1 -0.49, 0.15 -0.475, 0.2 -0.45, 0.25 -0.42, 0.3 -0.375, 0.35 -0.3, 0.4 -0.2, " +
    "0.4 0.5, -0.4 0.5",
  FTA_OR:
    "-0.4 0, -0.35 -0.115, -0.3 -0.215, -0.25 -0.28, -0.2 -0.34, -0.15 -0.395, -0.1 -0.435, -0.05 -0.47, 0 -0.5, " +
    "0.05 -0.47, 0.1 -0.435, 0.15 -0.395, 0.2 -0.34, 0.25 -0.28, 0.3 -0.215, 0.35 -0.115, 0.4 0, " +
    "0.4 0.5, 0.35 0.475, 0.3 0.455, 0.25 0.44, 0.2 0.425, 0.15 0.415, 0.1 0.41, 0.05 0.405, 0 0.4, " +
    "-0.05 0.405, -0.1 0.41, -0.15 0.415, -0.2 0.425, -0.25 0.44, -0.3 0.455, -0.35 0.475, -0.4 0.5",
  SC_STRATEGY: "-0.8 -0.8, 1 -0.8, 0.8 0.8, -1 0.8",
};

/**
 * TIM node configuration.
 */
export const TIM_NODE_SELECTOR = `node[graph='${"tim" as GraphMode}']`;

export const TIM_NODE_SHAPE = "round-rectangle";
export const TIM_NODE_HEIGHT = 150;
export const TIM_NODE_WIDTH = 250;
export const TIM_NODE_COLOR = "transparent";
export const TIM_NODE_BORDER_WIDTH = 0;
