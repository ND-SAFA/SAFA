import {
  ARTIFACT_BORDER_STYLE,
  ARTIFACT_BORDER_WIDTH,
  ARTIFACT_HEIGHT,
  ARTIFACT_PADDING,
  ARTIFACT_SHAPE,
  ARTIFACT_WIDTH,
  ARTIFACT_SELECTED_BORDER_WIDTH,
} from "@/cytoscape/styles/config/artifact-tree-config";
import {
  TRACE_COLOR,
  TRACE_STYLE,
  TRACE_WIDTH,
  GENERATED_TRACE_COLOR,
} from "@/cytoscape/styles/config/trace";
import { CytoStyleSheet } from "@/types/cytoscape";
import { Stylesheet } from "cytoscape";
import { ThemeColors } from "@/util";

export const GENERATED_LINK_SELECTOR = 'edge[traceType="GENERATED"]';
export const UNREVIEWED_LINK_SELECTOR = 'edge[approvalStatus="UNREVIEWED"]';
export const DECLINED_LINK_SELECTOR = 'edge[approvalStatus="DECLINED"]';
export const APPROVED_LINK_SELECTOR =
  'edge[traceType="GENERATED"][approvalStatus="APPROVED"]';

export const CytoscapeStyle: (Stylesheet | CytoStyleSheet)[] = [
  {
    selector: "edge",
    style: {
      "curve-style": TRACE_STYLE,
      width: TRACE_WIDTH,
      "line-color": TRACE_COLOR,
      "source-arrow-shape": "chevron",
      "source-arrow-color": TRACE_COLOR,
      "arrow-scale": 2,
    },
  },
  {
    selector: GENERATED_LINK_SELECTOR,
    style: {
      "line-color": GENERATED_TRACE_COLOR,
      "source-arrow-color": GENERATED_TRACE_COLOR,
    },
  },
  {
    selector: UNREVIEWED_LINK_SELECTOR,
    style: {
      "line-style": "dashed",
      "line-dash-pattern": [6, 3],
    },
  },
  {
    selector: APPROVED_LINK_SELECTOR,
    style: {
      "line-style": "solid",
    },
  },
  {
    selector: "node",
    style: {
      padding: ARTIFACT_PADDING,
      "background-color": ThemeColors.artifactDefault,
      shape: ARTIFACT_SHAPE,
      width: ARTIFACT_WIDTH + "px",
      height: ARTIFACT_HEIGHT + "px",
      "border-style": ARTIFACT_BORDER_STYLE,
      "border-width": ARTIFACT_BORDER_WIDTH,
      "border-color": "white", // ThemeColors.artifactBorder,
      "text-wrap": "ellipsis",
    },
  } as CytoStyleSheet,
  {
    selector: "node[?isSelected]",
    style: {
      "border-color": ThemeColors.artifactBorder,
      "border-width": ARTIFACT_SELECTED_BORDER_WIDTH,
    },
  },
  {
    selector: ".hidden",
    css: {
      display: "none",
    },
  },
];
