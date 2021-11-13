import { CytoStyleSheet } from "@/types/cytoscape";
import { Stylesheet } from "cytoscape";
import {
  TIM_EDGE_ARROW_SHAPE,
  TIM_EDGE_STYLE,
  TIM_EDGE_WIDTH,
  TIM_EDGE_X_MARGIN,
  TIM_NODE_BACKGROUND_COLOR,
  TIM_NODE_BORDER_COLOR,
  TIM_NODE_BORDER_WIDTH,
  TIM_NODE_HEIGHT,
  TIM_NODE_SHAPE,
  TIM_NODE_WIDTH,
} from "@/cytoscape/styles/config/tim-tree-config";

export const TimStyleSheets: (Stylesheet | CytoStyleSheet)[] = [
  {
    selector: "edge",
    style: {
      "curve-style": TIM_EDGE_STYLE,
      "source-arrow-shape": TIM_EDGE_ARROW_SHAPE,
      width: TIM_EDGE_WIDTH,
      label: "data(count)",
      "text-margin-x": TIM_EDGE_X_MARGIN,
    },
  },
  {
    selector: "node",
    style: {
      shape: TIM_NODE_SHAPE,
      width: TIM_NODE_WIDTH,
      height: TIM_NODE_HEIGHT,
      backgroundColor: TIM_NODE_BACKGROUND_COLOR,
      "border-color": TIM_NODE_BORDER_COLOR,
      "border-width": TIM_NODE_BORDER_WIDTH,
    },
  },
];
