import { ARTIFACT_HEIGHT, ARTIFACT_WIDTH } from "@/cytoscape/styles/config";
import { CytoStyleSheet } from "@/types/cytoscape";
import { Stylesheet } from "cytoscape";
import { ThemeColors } from "@/util";
import {
  ArtifactDeltaState,
  FTANodeType,
  SafetyCaseType,
  TraceApproval,
  TraceType,
} from "@/types";

export const GENERATED_LINK_SELECTOR = `edge[traceType='${TraceType.GENERATED}']`;

export const CytoscapeStyle: (Stylesheet | CytoStyleSheet)[] = [
  // Edges
  {
    selector: "edge",
    style: {
      width: "2px",
      "curve-style": "bezier",
      "line-color": ThemeColors.primary,
      "source-arrow-shape": "chevron",
      "source-arrow-color": ThemeColors.primary,
      "arrow-scale": 2,
    },
  },
  {
    selector: "edge[?faded]",
    style: { opacity: 0.1 },
  },
  // Edges - Generated
  {
    selector: GENERATED_LINK_SELECTOR,
    style: {
      "line-color": ThemeColors.secondary,
      "source-arrow-color": ThemeColors.secondary,
    },
  },
  {
    selector: `edge[approvalStatus='${TraceApproval.UNREVIEWED}']`,
    style: {
      "line-style": "dashed",
      "line-dash-pattern": [6, 3],
    },
  },
  {
    selector: `edge[traceType='${TraceType.GENERATED}'][approvalStatus='${TraceApproval.APPROVED}']`,
    style: {
      "line-style": "solid",
    },
  },
  // Edges - Delta
  {
    selector: `edge[deltaType='${ArtifactDeltaState.ADDED}']`,
    style: {
      "target-arrow-color": ThemeColors.artifactAdded,
      "source-arrow-color": ThemeColors.artifactAdded,
      "line-color": ThemeColors.artifactAdded,
    },
  },
  {
    selector: `edge[deltaType='${ArtifactDeltaState.MODIFIED}']`,
    style: {
      "target-arrow-color": ThemeColors.artifactModified,
      "source-arrow-color": ThemeColors.artifactModified,
      "line-color": ThemeColors.artifactModified,
    },
  },
  {
    selector: `edge[deltaType='${ArtifactDeltaState.REMOVED}']`,
    style: {
      "target-arrow-color": ThemeColors.artifactRemoved,
      "source-arrow-color": ThemeColors.artifactRemoved,
      "line-color": ThemeColors.artifactRemoved,
    },
  },
  // Nodes
  {
    selector: "node",
    style: {
      width: ARTIFACT_WIDTH + "px",
      height: ARTIFACT_HEIGHT + "px",
      padding: 50,
      "background-color": ThemeColors.artifactDefault,
      shape: "roundrectangle",
      "border-style": "solid",
      "border-width": 0,
      "border-color": ThemeColors.artifactBorder,
      "text-wrap": "ellipsis",
    },
  },
  {
    selector: "node[?isSelected]",
    style: {
      "border-width": 6,
    },
  },
  // Nodes - Delta
  {
    selector: `node[artifactDeltaState='${ArtifactDeltaState.ADDED}']`,
    style: {
      "background-color": ThemeColors.artifactAdded,
    },
  },
  {
    selector: `node[artifactDeltaState='${ArtifactDeltaState.MODIFIED}']`,
    style: {
      "background-color": ThemeColors.artifactModified,
    },
  },
  {
    selector: `node[artifactDeltaState='${ArtifactDeltaState.REMOVED}']`,
    style: {
      "background-color": ThemeColors.artifactRemoved,
    },
  },
  // Nodes - Logic
  {
    selector: `node[logicType='${FTANodeType.AND}']`,
    style: {
      shape: "polygon",
      "shape-polygon-points":
        "-0.4 -0.2, -0.35 -0.3, -0.3 -0.375, -0.25 -0.42, -0.2 -0.45, -0.15 -0.475, -0.1 -0.49, -0.05 -0.495, 0 -0.5, " +
        "0.05 -0.495, 0.1 -0.49, 0.15 -0.475, 0.2 -0.45, 0.25 -0.42, 0.3 -0.375, 0.35 -0.3, 0.4 -0.2, " +
        "0.4 0.5, -0.4 0.5",
      "border-width": "1",
    },
  },
  {
    selector: `node[logicType='${FTANodeType.OR}']`,
    style: {
      shape: "polygon",
      "shape-polygon-points":
        "-0.4 0, -0.35 -0.115, -0.3 -0.215, -0.25 -0.28, -0.2 -0.34, -0.15 -0.395, -0.1 -0.435, -0.05 -0.47, 0 -0.5, " +
        "0.05 -0.47, 0.1 -0.435, 0.15 -0.395, 0.2 -0.34, 0.25 -0.28, 0.3 -0.215, 0.35 -0.115, 0.4 0, " +
        "0.4 0.5, 0.35 0.475, 0.3 0.455, 0.25 0.44, 0.2 0.425, 0.15 0.415, 0.1 0.41, 0.05 0.405, 0 0.4, " +
        "-0.05 0.405, -0.1 0.41, -0.15 0.415, -0.2 0.425, -0.25 0.44, -0.3 0.455, -0.35 0.475, -0.4 0.5",
      "border-width": "1",
    },
  },
  // Nodes - Safety Case
  {
    selector: `node[safetyCaseType='${SafetyCaseType.GOAL}']`,
    style: {
      shape: "rectangle",
      "border-width": "1",
      width: ARTIFACT_WIDTH,
      height: ARTIFACT_HEIGHT,
    },
  },
  {
    selector: `node[safetyCaseType='${SafetyCaseType.CONTEXT}']`,
    style: {
      shape: "roundrectangle",
      "border-width": "1",
      width: ARTIFACT_WIDTH,
      height: ARTIFACT_HEIGHT,
    },
  },
  {
    selector: `node[safetyCaseType='${SafetyCaseType.SOLUTION}']`,
    style: {
      shape: "ellipse",
      "border-width": "1",
      width: ARTIFACT_HEIGHT * 1.4,
      height: ARTIFACT_HEIGHT * 1.4,
    },
  },
  {
    selector: `node[safetyCaseType='${SafetyCaseType.STRATEGY}']`,
    style: {
      shape: "polygon",
      "shape-polygon-points": "-0.8 -0.8, 1 -0.8, 0.8 0.8, -1 0.8",
      "border-width": "1",
      width: ARTIFACT_WIDTH * 1.2,
      height: ARTIFACT_HEIGHT * 1.65,
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
