import { Stylesheet } from "cytoscape";
import { GraphMode } from "@/types";
import { ThemeColors } from "@/util";
import { CytoStyleSheet } from "@/types/cytoscape";
import {
  TIM_EDGE_ARROW_SHAPE,
  TIM_EDGE_STYLE,
  TIM_EDGE_WIDTH,
  TIM_EDGE_X_MARGIN,
  TIM_NODE_BORDER_WIDTH,
  TIM_NODE_COLOR,
  TIM_NODE_HEIGHT,
  TIM_NODE_SHAPE,
  TIM_NODE_WIDTH,
} from "@/cytoscape/styles/config/tim-tree-config";

export const TIM_NODE_SELECTOR = `node[graph='${GraphMode.tim}']`;
export const TIM_EDGE_SELECTOR = `edge[graph='${GraphMode.tim}']`;

export const TimStyleSheets: (Stylesheet | CytoStyleSheet)[] = [
  // Edges
  {
    selector: TIM_EDGE_SELECTOR,
    style: {
      "curve-style": TIM_EDGE_STYLE,
      "source-arrow-shape": TIM_EDGE_ARROW_SHAPE,
      width: TIM_EDGE_WIDTH,
      label: "data(count)",
      "text-margin-x": TIM_EDGE_X_MARGIN,
    },
  },
  {
    selector: ".loop",
    style: {
      "control-point-step-size": 120,
    },
  },
  // Nodes
  {
    selector: TIM_NODE_SELECTOR,
    style: {
      shape: TIM_NODE_SHAPE,
      width: TIM_NODE_WIDTH,
      height: TIM_NODE_HEIGHT,
      "background-color": ThemeColors.lightGrey,
      "border-width": TIM_NODE_BORDER_WIDTH,
      "border-color": TIM_NODE_COLOR,
    },
  },
];
