import { Stylesheet } from "cytoscape";
import { CytoStyleSheet } from "@/types/cytoscape/core";
import {
  LINE_GHOST_COLOR,
  LINE_PREVIEW_COLOR,
  SOURCE_SELECTION_COLOR,
  SOURCE_SELECTION_WIDTH,
  TARGET_SELECTION_COLOR,
  TARGET_SELECTION_WIDTH,
} from "@/cytoscape/styles/config/edge-handles";

export const EdgeHandlesStyle: (Stylesheet | CytoStyleSheet)[] = [
  {
    selector: ".eh-hover",
    style: {},
  },
  {
    selector: ".eh-source",
    style: {
      "border-width": SOURCE_SELECTION_WIDTH,
      "border-color": SOURCE_SELECTION_COLOR,
    },
  },
  {
    selector: ".eh-target",
    style: {
      "border-width": TARGET_SELECTION_WIDTH,
      "border-color": TARGET_SELECTION_COLOR,
    },
  },
  {
    selector: ".eh-ghost-edge",
    style: {
      "line-fill": "linear-gradient",
      "line-gradient-stop-colors": "cyan magenta yellow",
      "line-style": "dotted",
      "line-dash-pattern": [6, 3],
      "line-color": LINE_GHOST_COLOR,
      "source-arrow-shape": "none",
      "target-arrow-shape": "chevron",
    },
  },
  {
    selector: ".eh-preview",
    style: {
      "line-color": LINE_PREVIEW_COLOR,
      "source-arrow-shape": "none",
      "target-arrow-shape": "chevron",
    },
  },
  {
    selector: ".eh-ghost-node",
    style: {
      opacity: 0,
    },
  },
  {
    selector: ".eh-ghost-edge.eh-preview-active",
    style: {
      opacity: 0,
    },
  },
];
