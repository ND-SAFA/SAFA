import { CytoStyleSheet } from "@/types/cytoscape";
import { Stylesheet } from "cytoscape";
import {
  TIM_NODE_HEIGHT,
  TIM_NODE_WIDTH,
} from "@/cytoscape/styles/config/tim-tree-config";

export const TimStyleSheets: (Stylesheet | CytoStyleSheet)[] = [
  {
    selector: "edge",
    style: {
      "curve-style": "taxi",
      "source-arrow-shape": "chevron",
      width: "2",
    },
  },
  {
    selector: "node",
    style: {
      shape: "rectangle",
      width: TIM_NODE_WIDTH,
      height: TIM_NODE_HEIGHT,
      backgroundColor: "white",
      "border-color": "black",
      "border-width": "1",
    },
  },
];
