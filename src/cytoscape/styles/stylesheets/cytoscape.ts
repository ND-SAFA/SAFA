import {
  ARTIFACT_ADDED_COLOR,
  ARTIFACT_BORDER_STYLE,
  ARTIFACT_BORDER_WIDTH,
  ARTIFACT_BACKGROUND_COLOR,
  ARTIFACT_HEIGHT,
  ARTIFACT_MODIFIED_COLOR,
  ARTIFACT_PADDING,
  ARTIFACT_REMOVED_COLOR as NODE_REMOVED_COLOR,
  ARTIFACT_SHAPE,
  ARTIFACT_WIDTH,
  ARTIFACT_SELECTED_COLOR,
  ARTIFACT_SELECTED_BORDER_WIDTH,
} from "@/cytoscape/styles/config/artifact-tree-config";
import {
  TRACE_COLOR,
  TRACE_STYLE,
  TRACE_WIDTH,
  GENERATED_TRACE_COLOR,
} from "@/cytoscape/styles/config/trace";
import { ArtifactDeltaState } from "@/types/domain";
import { CytoStyleSheet } from "@/types/cytoscape";
import { Stylesheet } from "cytoscape";

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
      "background-color": ARTIFACT_BACKGROUND_COLOR,
      shape: ARTIFACT_SHAPE,
      width: ARTIFACT_WIDTH + "px",
      height: ARTIFACT_HEIGHT + "px",
      "border-style": ARTIFACT_BORDER_STYLE,
      "border-width": ARTIFACT_BORDER_WIDTH,
      "text-wrap": "ellipsis",
    },
  } as CytoStyleSheet,
  {
    selector: "node[?isSelected]",
    style: {
      "border-color": ARTIFACT_SELECTED_COLOR,
      "border-width": ARTIFACT_SELECTED_BORDER_WIDTH,
    },
  },
  {
    selector: `node[artifactDeltaState="${ArtifactDeltaState.ADDED}"]`,
    style: {
      "background-color": ARTIFACT_ADDED_COLOR,
    },
  },
  {
    selector: `node[artifactDeltaState="${ArtifactDeltaState.REMOVED}"]`,
    style: {
      "background-color": NODE_REMOVED_COLOR,
    },
  },
  {
    selector: `node[artifactDeltaState="${ArtifactDeltaState.MODIFIED}"]`,
    style: {
      "background-color": ARTIFACT_MODIFIED_COLOR,
    },
  },
  {
    selector: ".hidden",
    css: {
      display: "none",
    },
  },
];
