"use strict";
exports.__esModule = true;
exports.TimKlaySettings = void 0;
var styles_1 = require("@/cytoscape/styles");
// docs: https://github.com/cytoscape/cytoscape.js-klay
exports.TimKlaySettings = {
    spacing: styles_1.TIM_GRAPH_NODE_SPACING,
    direction: styles_1.LAYOUT_NODE_DIRECTION,
    fixedAlignment: styles_1.LAYOUT_ALIGNMENT,
    layoutHierarchy: styles_1.LAYOUT_USE_HIERARCHY,
    nodeLayering: styles_1.LAYOUT_NODE_LAYERING,
    nodePlacement: styles_1.LAYOUT_NODE_PLACEMENT,
    thoroughness: styles_1.LAYOUT_THOROUGHNESS,
    randomizationSeed: styles_1.LAYOUT_RANDOM_SEED
};
