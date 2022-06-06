"use strict";
exports.__esModule = true;
exports.LAYOUT_RANDOM_SEED = exports.LAYOUT_THOROUGHNESS = exports.LAYOUT_NODE_INNER_SPACING = exports.LAYOUT_NODE_PLACEMENT = exports.LAYOUT_NODE_LAYERING = exports.LAYOUT_USE_HIERARCHY = exports.LAYOUT_ALIGNMENT = exports.LAYOUT_NODE_DIRECTION = exports.LAYOUT_NODE_SPACING = exports.DEFAULT_ARTIFACT_TREE_ZOOM = exports.CENTER_GRAPH_PADDING = exports.ARTIFACT_HEIGHT = exports.ARTIFACT_WIDTH = void 0;
var types_1 = require("@/types");
/**
 * Artifact node fields.
 */
exports.ARTIFACT_WIDTH = 105;
exports.ARTIFACT_HEIGHT = (exports.ARTIFACT_WIDTH * 9) / 16;
/**
 * Graph specific values.
 */
exports.CENTER_GRAPH_PADDING = 10;
exports.DEFAULT_ARTIFACT_TREE_ZOOM = 0.75;
/**
 * Layout Options.
 */
exports.LAYOUT_NODE_SPACING = 20;
exports.LAYOUT_NODE_DIRECTION = types_1.LayoutDirection.DOWN;
exports.LAYOUT_ALIGNMENT = types_1.FixedAlignment.BALANCED;
exports.LAYOUT_USE_HIERARCHY = true;
exports.LAYOUT_NODE_LAYERING = types_1.NodeLayering.NETWORK_SIMPLEX;
exports.LAYOUT_NODE_PLACEMENT = types_1.NodePlacement.BRANDES_KOEPF;
// Factor by which the usual spacing is multiplied to determine the in-layer spacing between objects.
exports.LAYOUT_NODE_INNER_SPACING = 0.4;
// How much effort should be spent to produce a nice layout.
exports.LAYOUT_THOROUGHNESS = 10;
exports.LAYOUT_RANDOM_SEED = 42;
