"use strict";
exports.__esModule = true;
exports.EdgeHandlesStyle = void 0;
var edge_handles_1 = require("@/cytoscape/styles/config/edge-handles");
exports.EdgeHandlesStyle = [
    {
        selector: ".eh-hover",
        style: {}
    },
    {
        selector: ".eh-source",
        style: {
            "border-width": edge_handles_1.SOURCE_SELECTION_WIDTH,
            "border-color": edge_handles_1.SOURCE_SELECTION_COLOR
        }
    },
    {
        selector: ".eh-target",
        style: {
            "border-width": edge_handles_1.TARGET_SELECTION_WIDTH,
            "border-color": edge_handles_1.TARGET_SELECTION_COLOR
        }
    },
    {
        selector: ".eh-ghost-edge",
        style: {
            "line-fill": "linear-gradient",
            "line-gradient-stop-colors": "cyan magenta yellow",
            "line-style": "dotted",
            "line-dash-pattern": [6, 3],
            "line-color": edge_handles_1.LINE_GHOST_COLOR,
            "source-arrow-shape": "none",
            "target-arrow-shape": "chevron"
        }
    },
    {
        selector: ".eh-preview",
        style: {
            "line-color": edge_handles_1.LINE_PREVIEW_COLOR,
            "source-arrow-shape": "none",
            "target-arrow-shape": "chevron"
        }
    },
    {
        selector: ".eh-ghost-node",
        style: {
            opacity: 0
        }
    },
    {
        selector: ".eh-ghost-edge.eh-preview-active",
        style: {
            opacity: 0
        }
    },
];
