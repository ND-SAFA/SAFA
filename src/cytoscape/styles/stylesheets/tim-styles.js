"use strict";
exports.__esModule = true;
exports.TimStyleSheets = void 0;
var tim_tree_config_1 = require("@/cytoscape/styles/config/tim-tree-config");
exports.TimStyleSheets = [
    {
        selector: "edge",
        style: {
            "curve-style": tim_tree_config_1.TIM_EDGE_STYLE,
            "source-arrow-shape": tim_tree_config_1.TIM_EDGE_ARROW_SHAPE,
            width: tim_tree_config_1.TIM_EDGE_WIDTH,
            label: "data(count)",
            "text-margin-x": tim_tree_config_1.TIM_EDGE_X_MARGIN
        }
    },
    {
        selector: ".loop",
        style: {
            "control-point-step-size": 120
        }
    },
    {
        selector: "node",
        style: {
            shape: tim_tree_config_1.TIM_NODE_SHAPE,
            width: tim_tree_config_1.TIM_NODE_WIDTH,
            height: tim_tree_config_1.TIM_NODE_HEIGHT,
            backgroundColor: "white",
            "border-width": tim_tree_config_1.TIM_NODE_BORDER_WIDTH,
            "border-color": tim_tree_config_1.TIM_NODE_COLOR
        }
    },
];
