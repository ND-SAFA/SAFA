import { ApprovalType, ArtifactDeltaState, CytoStyleSheet } from "@/types";
import {
  EDGE_COLOR,
  EDGE_WIDTH,
  TIM_EDGE_SELECTOR,
  TRACE_CURVE_STYLE,
  ARTIFACT_EDGE_SELECTOR,
  GENERATED_APPROVED_LINK_SELECTOR,
  GENERATED_LINK_SELECTOR,
  EDGE_SHAPE,
  TIM_EDGE_STYLE,
  TIM_EDGE_ARROW_SHAPE,
  TIM_EDGE_X_MARGIN,
  EDGE_ARROW_SCALE,
  TRACE_FADED_OPACITY,
  TRACE_LINE_STYLE,
  TIM_EDGE_FONT_WEIGHT,
  TIM_EDGE_FONT_SIZE,
  TIM_EDGE_LOOP_STEP_SIZE,
  NODE_BG_COLOR,
  TIM_EDGE_FONT_BG_OPACITY,
} from "@/cytoscape/styles/config";

export const edgeStyles: CytoStyleSheet[] = [
  // Trace Links
  {
    selector: ARTIFACT_EDGE_SELECTOR,
    style: {
      width: EDGE_WIDTH,
      "curve-style": TRACE_CURVE_STYLE,
      "line-color": EDGE_COLOR.DEFAULT,
      "source-arrow-shape": EDGE_SHAPE.TARGET,
      "target-arrow-shape": EDGE_SHAPE.SOURCE,
      "source-arrow-color": EDGE_COLOR.DEFAULT,
      "arrow-scale": EDGE_ARROW_SCALE,
    },
  },
  {
    selector: `${ARTIFACT_EDGE_SELECTOR}[?faded]`,
    style: { opacity: TRACE_FADED_OPACITY },
  },
  // Generated Trace Links
  {
    selector: GENERATED_LINK_SELECTOR,
    style: {
      "line-color": EDGE_COLOR.GENERATED,
      "source-arrow-color": EDGE_COLOR.GENERATED,
    },
  },
  {
    selector: `${ARTIFACT_EDGE_SELECTOR}[approvalStatus='${
      "UNREVIEWED" as ApprovalType
    }']`,
    style: {
      "line-style": TRACE_LINE_STYLE.UNREVIEWED,
      "line-dash-pattern": [6, 3],
    },
  },
  {
    selector: GENERATED_APPROVED_LINK_SELECTOR,
    style: {
      "line-style": TRACE_LINE_STYLE.DEFAULT,
    },
  },
  // Trace Link Delta
  {
    selector: `${ARTIFACT_EDGE_SELECTOR}[deltaType='${
      "NO_CHANGE" as ArtifactDeltaState
    }']`,
    style: {
      "target-arrow-color": EDGE_COLOR.NO_CHANGE,
      "source-arrow-color": EDGE_COLOR.NO_CHANGE,
      "line-color": EDGE_COLOR.NO_CHANGE,
    },
  },
  {
    selector: `${ARTIFACT_EDGE_SELECTOR}[deltaType='${
      "ADDED" as ArtifactDeltaState
    }']`,
    style: {
      "target-arrow-color": EDGE_COLOR.ADDED,
      "source-arrow-color": EDGE_COLOR.ADDED,
      "line-color": EDGE_COLOR.ADDED,
    },
  },
  {
    selector: `${ARTIFACT_EDGE_SELECTOR}[deltaType='${
      "MODIFIED" as ArtifactDeltaState
    }']`,
    style: {
      "target-arrow-color": EDGE_COLOR.MODIFIED,
      "source-arrow-color": EDGE_COLOR.MODIFIED,
      "line-color": EDGE_COLOR.MODIFIED,
    },
  },
  {
    selector: `${GENERATED_APPROVED_LINK_SELECTOR}[deltaType='${
      "MODIFIED" as ArtifactDeltaState
    }']`,
    style: {
      "target-arrow-color": EDGE_COLOR.ADDED,
      "source-arrow-color": EDGE_COLOR.ADDED,
      "line-color": EDGE_COLOR.ADDED,
    },
  },
  {
    selector: `${ARTIFACT_EDGE_SELECTOR}[deltaType='${
      "REMOVED" as ArtifactDeltaState
    }']`,
    style: {
      "target-arrow-color": EDGE_COLOR.REMOVED,
      "source-arrow-color": EDGE_COLOR.REMOVED,
      "line-color": EDGE_COLOR.REMOVED,
    },
  },
  // Edge Creation Handles
  {
    selector: ".eh-hover",
    style: {},
  },
  {
    selector: ".eh-source",
    style: {
      "border-width": EDGE_WIDTH,
      "border-color": EDGE_COLOR.GENERATED,
    },
  },
  {
    selector: ".eh-target",
    style: {
      "border-width": EDGE_WIDTH,
      "border-color": EDGE_COLOR.GENERATED,
    },
  },
  {
    selector: ".eh-ghost-edge",
    style: {
      "line-fill": "linear-gradient",
      "line-gradient-stop-colors": "cyan magenta yellow",
      "line-style": TRACE_LINE_STYLE.CREATION,
      "line-dash-pattern": [6, 3],
      "line-color": EDGE_COLOR.GHOST,
      "source-arrow-shape": EDGE_SHAPE.SOURCE,
      "target-arrow-shape": EDGE_SHAPE.TARGET,
    },
  },
  {
    selector: ".eh-preview",
    style: {
      "line-color": EDGE_COLOR.GENERATED,
      "source-arrow-shape": EDGE_SHAPE.SOURCE,
      "target-arrow-shape": EDGE_SHAPE.TARGET,
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
  // TIM Edges
  {
    selector: TIM_EDGE_SELECTOR,
    style: {
      "curve-style": TIM_EDGE_STYLE,
      "source-arrow-shape": TIM_EDGE_ARROW_SHAPE,
      width: EDGE_WIDTH,
      "text-margin-x": TIM_EDGE_X_MARGIN,
      "source-arrow-color": EDGE_COLOR.DEFAULT,
      "line-color": EDGE_COLOR.DEFAULT,
      "font-weight": TIM_EDGE_FONT_WEIGHT,
      "font-size": TIM_EDGE_FONT_SIZE,
      "text-background-opacity": TIM_EDGE_FONT_BG_OPACITY,
      "text-background-color": NODE_BG_COLOR.LIGHT,
      label: "data(label)",
    },
  },
  {
    selector: `${TIM_EDGE_SELECTOR}[?dark]`,
    style: {
      "text-background-color": NODE_BG_COLOR.DARK,
      color: NODE_BG_COLOR.LIGHT,
    },
  },
  {
    selector: `${TIM_EDGE_SELECTOR}[?generated]`,
    style: {
      "line-color": EDGE_COLOR.GENERATED,
      "source-arrow-color": EDGE_COLOR.GENERATED,
    },
  },
  {
    selector: ".loop",
    style: {
      "control-point-step-size": TIM_EDGE_LOOP_STEP_SIZE,
      "loop-direction": "-90deg",
      "loop-sweep": "40deg",
      "target-endpoint": "outside-to-line",
      "source-endpoint": "outside-to-line",
    },
  },
];
