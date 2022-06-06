"use strict";
exports.__esModule = true;
exports.CytoscapeStyle = exports.GENERATED_LINK_SELECTOR = void 0;
var config_1 = require("@/cytoscape/styles/config");
var util_1 = require("@/util");
var types_1 = require("@/types");
exports.GENERATED_LINK_SELECTOR = "edge[traceType='" + types_1.TraceType.GENERATED + "']";
exports.CytoscapeStyle = [
    // Edges
    {
        selector: "edge",
        style: {
            width: "2px",
            "curve-style": "bezier",
            "line-color": util_1.ThemeColors.primary,
            "source-arrow-shape": "chevron",
            "source-arrow-color": util_1.ThemeColors.primary,
            "arrow-scale": 2
        }
    },
    {
        selector: "edge[?faded]",
        style: { opacity: 0.1 }
    },
    // Edges - Generated
    {
        selector: exports.GENERATED_LINK_SELECTOR,
        style: {
            "line-color": util_1.ThemeColors.secondary,
            "source-arrow-color": util_1.ThemeColors.secondary
        }
    },
    {
        selector: "edge[approvalStatus='" + types_1.TraceApproval.UNREVIEWED + "']",
        style: {
            "line-style": "dashed",
            "line-dash-pattern": [6, 3]
        }
    },
    {
        selector: "edge[traceType='" + types_1.TraceType.GENERATED + "'][approvalStatus='" + types_1.TraceApproval.APPROVED + "']",
        style: {
            "line-style": "solid"
        }
    },
    // Edges - Delta
    {
        selector: "edge[deltaType='" + types_1.ArtifactDeltaState.ADDED + "']",
        style: {
            "target-arrow-color": util_1.ThemeColors.artifactAdded,
            "source-arrow-color": util_1.ThemeColors.artifactAdded,
            "line-color": util_1.ThemeColors.artifactAdded
        }
    },
    {
        selector: "edge[deltaType='" + types_1.ArtifactDeltaState.MODIFIED + "']",
        style: {
            "target-arrow-color": util_1.ThemeColors.artifactModified,
            "source-arrow-color": util_1.ThemeColors.artifactModified,
            "line-color": util_1.ThemeColors.artifactModified
        }
    },
    {
        selector: "edge[deltaType='" + types_1.ArtifactDeltaState.REMOVED + "']",
        style: {
            "target-arrow-color": util_1.ThemeColors.artifactRemoved,
            "source-arrow-color": util_1.ThemeColors.artifactRemoved,
            "line-color": util_1.ThemeColors.artifactRemoved
        }
    },
    // Nodes
    {
        selector: "node",
        style: {
            width: config_1.ARTIFACT_WIDTH + "px",
            height: config_1.ARTIFACT_HEIGHT + "px",
            padding: 50,
            "background-color": util_1.ThemeColors.artifactDefault,
            shape: "roundrectangle",
            "border-style": "solid",
            "border-width": 0,
            "border-color": util_1.ThemeColors.artifactBorder,
            "text-wrap": "ellipsis"
        }
    },
    {
        selector: "node[?isSelected]",
        style: {
            "border-width": 6
        }
    },
    // Nodes - Delta
    {
        selector: "node[artifactDeltaState='" + types_1.ArtifactDeltaState.ADDED + "']",
        style: {
            "background-color": util_1.ThemeColors.artifactAdded
        }
    },
    {
        selector: "node[artifactDeltaState='" + types_1.ArtifactDeltaState.MODIFIED + "']",
        style: {
            "background-color": util_1.ThemeColors.artifactModified
        }
    },
    {
        selector: "node[artifactDeltaState='" + types_1.ArtifactDeltaState.REMOVED + "']",
        style: {
            "background-color": util_1.ThemeColors.artifactRemoved
        }
    },
    // Nodes - Logic
    {
        selector: "node[logicType='" + types_1.FTANodeType.AND + "']",
        style: {
            shape: "polygon",
            // Full size:
            // "shape-polygon-points":
            //   "-0.8 -0.4, -0.7 -0.6, -0.6 -0.75, -0.5 -0.84, -0.4 -0.9, -0.3 -0.95, -0.2 -0.98, -0.1 -0.99, 0 -1, " +
            //   "0.1 -0.99, 0.2 -0.98, 0.3 -0.95, 0.4 -0.9, 0.5 -0.84, 0.6 -0.75, 0.7 -0.6, 0.8 -0.4, " +
            //   "0.8 1, -0.8 1",
            // Half size:
            "shape-polygon-points": "-0.4 -0.2, -0.35 -0.3, -0.3 -0.375, -0.25 -0.42, -0.2 -0.45, -0.15 -0.475, -0.1 -0.49, -0.05 -0.495, 0 -0.5, " +
                "0.05 -0.495, 0.1 -0.49, 0.15 -0.475, 0.2 -0.45, 0.25 -0.42, 0.3 -0.375, 0.35 -0.3, 0.4 -0.2, " +
                "0.4 0.5, -0.4 0.5",
            "border-width": "1"
        }
    },
    {
        selector: "node[logicType='" + types_1.FTANodeType.OR + "']",
        style: {
            shape: "polygon",
            // Full size:
            // "shape-polygon-points":
            //   "-0.8 0, -0.7 -0.23, -0.6 -0.43, -0.5 -0.56, -0.4 -0.68, -0.3 -0.79, -0.2 -0.87, -0.1 -0.94, 0 -1, " +
            //   "0.1 -0.94, 0.2 -0.87, 0.3 -0.79, 0.4 -0.68, 0.5 -0.56, 0.6 -0.43, 0.7 -0.23, 0.8 0, " +
            //   "0.8 1, 0.7 0.95, 0.6 0.91, 0.5 0.88, 0.4 0.85, 0.3 0.83, 0.2 0.82, 0.1 0.81, 0 0.8, " +
            //   "-0.1 0.81, -0.2 0.82, -0.3 0.83, -0.4 0.85, -0.5 0.88, -0.6 0.91, -0.7 0.95, -0.8 1",
            // Half size:
            "shape-polygon-points": "-0.4 0, -0.35 -0.115, -0.3 -0.215, -0.25 -0.28, -0.2 -0.34, -0.15 -0.395, -0.1 -0.435, -0.05 -0.47, 0 -0.5, " +
                "0.05 -0.47, 0.1 -0.435, 0.15 -0.395, 0.2 -0.34, 0.25 -0.28, 0.3 -0.215, 0.35 -0.115, 0.4 0, " +
                "0.4 0.5, 0.35 0.475, 0.3 0.455, 0.25 0.44, 0.2 0.425, 0.15 0.415, 0.1 0.41, 0.05 0.405, 0 0.4, " +
                "-0.05 0.405, -0.1 0.41, -0.15 0.415, -0.2 0.425, -0.25 0.44, -0.3 0.455, -0.35 0.475, -0.4 0.5",
            "border-width": "1"
        }
    },
    // Nodes - Safety Case
    {
        selector: "node[safetyCaseType='" + types_1.SafetyCaseType.GOAL + "']",
        style: {
            shape: "polygon",
            "shape-polygon-points": "-1 -0.8, 1 -0.8, 1 0.8, -1 0.8",
            "border-width": "1"
        }
    },
    {
        selector: "node[safetyCaseType='" + types_1.SafetyCaseType.SOLUTION + "']",
        style: {
            height: 50,
            width: 50,
            shape: "ellipse",
            "border-width": "1"
        }
    },
    {
        selector: "node[safetyCaseType='" + types_1.SafetyCaseType.CONTEXT + "']",
        style: {
            height: 30,
            shape: "roundrectangle",
            "border-width": "1"
        }
    },
    {
        selector: "node[safetyCaseType='" + types_1.SafetyCaseType.STRATEGY + "']",
        style: {
            shape: "polygon",
            "shape-polygon-points": "-0.8 -0.8, 1 -0.8, 0.8 0.8, -1 0.8",
            "border-width": "1"
        }
    },
    // Misc
    {
        selector: ".hidden",
        css: {
            display: "none"
        }
    },
];
