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
        "-0.8 -0.4, -0.7 -0.6, -0.6 -0.75, -0.5 -0.84, -0.4 -0.9, -0.3 -0.95, -0.2 -0.98, -0.1 -0.99, 0 -1, " +
        "0.1 -0.99, 0.2 -0.98, 0.3 -0.95, 0.4 -0.9, 0.5 -0.84, 0.6 -0.75, 0.7 -0.6, 0.8 -0.4, " +
        "0.8 1, -0.8 1",
      "border-width": "1",
    },
  },
  {
    selector: `node[logicType='${FTANodeType.OR}']`,
    style: {
      shape: "polygon",
      "shape-polygon-points":
        "-0.8 0, -0.7 -0.23, -0.6 -0.43, -0.5 -0.56, -0.4 -0.68, -0.3 -0.79, -0.2 -0.87, -0.1 -0.94, 0 -1, " +
        "0.1 -0.94, 0.2 -0.87, 0.3 -0.79, 0.4 -0.68, 0.5 -0.56, 0.6 -0.43, 0.7 -0.23, 0.8 0, " +
        "0.8 1, 0.7 0.95, 0.6 0.91, 0.5 0.88, 0.4 0.85, 0.3 0.83, 0.2 0.82, 0.1 0.81, 0 0.8, " +
        "-0.1 0.81, -0.2 0.82, -0.3 0.83, -0.4 0.85, -0.5 0.88, -0.6 0.91, -0.7 0.95, -0.8 1",
      "border-width": "1",
    },
  },
  // Nodes - Safety Case
  {
    selector: `node[safetyCaseType='${SafetyCaseType.GOAL}']`,
    style: {
      shape: "polygon",
      "shape-polygon-points": "-1 -0.8, 1 -0.8, 1 0.8, -1 0.8",
      "border-width": "1",
    },
  },
  {
    selector: `node[safetyCaseType='${SafetyCaseType.SOLUTION}']`,
    style: {
      height: 50,
      width: 50,
      shape: "ellipse",
      "border-width": "1",
    },
  },
  {
    selector: `node[safetyCaseType='${SafetyCaseType.CONTEXT}']`,
    style: {
      height: 30,
      shape: "roundrectangle",
      "border-width": "1",
    },
  },
  {
    selector: `node[safetyCaseType='${SafetyCaseType.STRATEGY}']`,
    style: {
      shape: "polygon",
      "shape-polygon-points": "-0.8 -0.8, 1 -0.8, 0.8 0.8, -1 0.8",
      "border-width": "1",
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
