import { CytoStyleSheet, FTANodeType, SafetyCaseType } from "@/types";
import {
  TIM_NODE_SELECTOR,
  NODE_BG_COLOR,
  NODE_BORDER_COLOR,
  ARTIFACT_BORDER_STYLE,
  ARTIFACT_HEIGHT,
  ARTIFACT_NODE_SELECTOR,
  ARTIFACT_PADDING,
  ARTIFACT_SHAPE,
  ARTIFACT_WIDTH,
  NODE_BORDER_WIDTH,
  ARTIFACT_FTA_BORDER_WIDTH,
  ARTIFACT_POLYGONS,
  TIM_NODE_SHAPE,
  TIM_NODE_WIDTH,
  TIM_NODE_HEIGHT,
  TIM_NODE_BORDER_WIDTH,
  TIM_NODE_COLOR,
} from "@/cytoscape/styles/config";

export const nodeStyles: CytoStyleSheet[] = [
  // Artifacts
  {
    selector: ARTIFACT_NODE_SELECTOR,
    style: {
      width: ARTIFACT_WIDTH,
      height: ARTIFACT_HEIGHT,
      padding: ARTIFACT_PADDING,
      shape: ARTIFACT_SHAPE.DEFAULT,
      "background-color": NODE_BG_COLOR.LIGHT,
      "border-style": ARTIFACT_BORDER_STYLE,
      "border-width": NODE_BORDER_WIDTH,
      "border-color": NODE_BORDER_COLOR,
    },
  },
  {
    selector: `${ARTIFACT_NODE_SELECTOR}[?dark]`,
    style: {
      "background-color": NODE_BG_COLOR.DARK,
    },
  },
  // FTA Logic
  {
    selector: `${ARTIFACT_NODE_SELECTOR}[logicType='${"AND" as FTANodeType}']`,
    style: {
      "border-width": ARTIFACT_FTA_BORDER_WIDTH,
      shape: ARTIFACT_SHAPE.FTA,
      "shape-polygon-points": ARTIFACT_POLYGONS.FTA_AND,
    },
  },
  {
    selector: `${ARTIFACT_NODE_SELECTOR}[logicType='${"OR" as FTANodeType}']`,
    style: {
      "border-width": ARTIFACT_FTA_BORDER_WIDTH,
      shape: ARTIFACT_SHAPE.FTA,
      "shape-polygon-points": ARTIFACT_POLYGONS.FTA_OR,
    },
  },
  // Safety Cases
  {
    selector: `${ARTIFACT_NODE_SELECTOR}[safetyCaseType='${
      "GOAL" as SafetyCaseType
    }']`,
    style: {
      shape: ARTIFACT_SHAPE.SC_GOAL,
      width: ARTIFACT_WIDTH,
      height: ARTIFACT_HEIGHT,
    },
  },
  {
    selector: `${ARTIFACT_NODE_SELECTOR}[safetyCaseType='${
      "CONTEXT" as SafetyCaseType
    }']`,
    style: {
      shape: ARTIFACT_SHAPE.SC_CONTEXT,
      width: ARTIFACT_WIDTH,
      height: ARTIFACT_HEIGHT,
    },
  },
  {
    selector: `${ARTIFACT_NODE_SELECTOR}[safetyCaseType='${
      "SOLUTION" as SafetyCaseType
    }']`,
    style: {
      shape: ARTIFACT_SHAPE.SC_SOLUTION,
      width: ARTIFACT_HEIGHT * 1.4,
      height: ARTIFACT_HEIGHT * 1.4,
    },
  },
  {
    selector: `${ARTIFACT_NODE_SELECTOR}[safetyCaseType='${
      "STRATEGY" as SafetyCaseType
    }']`,
    style: {
      shape: ARTIFACT_SHAPE.SC_STRATEGY,
      width: ARTIFACT_WIDTH * 1.2,
      height: ARTIFACT_HEIGHT * 1.65,
      "shape-polygon-points": ARTIFACT_POLYGONS.SC_STRATEGY,
    },
  },
  // Tim Nodes
  {
    selector: TIM_NODE_SELECTOR,
    style: {
      shape: TIM_NODE_SHAPE,
      width: TIM_NODE_WIDTH,
      height: TIM_NODE_HEIGHT,
      "background-color": NODE_BG_COLOR.LIGHT,
      "border-width": TIM_NODE_BORDER_WIDTH,
      "border-color": TIM_NODE_COLOR,
    },
  },
  {
    selector: `${TIM_NODE_SELECTOR}[?dark]`,
    style: {
      "background-color": NODE_BG_COLOR.DARK,
    },
  },
  // Misc
  {
    selector: ".hidden",
    css: {
      display: "none",
    },
  },
];
