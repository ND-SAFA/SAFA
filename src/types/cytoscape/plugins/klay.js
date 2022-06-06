"use strict";
exports.__esModule = true;
exports.NodePlacement = exports.NodeLayering = exports.FixedAlignment = exports.LayoutDirection = void 0;
/**
 * Types were extracted from: https://github.com/cytoscape/cytoscape.js-klay
 */
/**
 * Enumerates the overall direction of edges: horizontal (right / left) or vertical (down / up).
 */
var LayoutDirection;
(function (LayoutDirection) {
    LayoutDirection["UNDEFINED"] = "UNDEFINED";
    LayoutDirection["RIGHT"] = "RIGHT";
    LayoutDirection["LEFT"] = "LEFT";
    LayoutDirection["DOWN"] = "DOWN";
    LayoutDirection["UP"] = "UP";
})(LayoutDirection = exports.LayoutDirection || (exports.LayoutDirection = {}));
/**
 * Enumerates the alignment to tell the BK node placer to use a certain alignment instead of taking the optimal result.
 */
var FixedAlignment;
(function (FixedAlignment) {
    /**
     * Chooses the smallest layout from the four possible candidates.
     */
    FixedAlignment["NONE"] = "NONE";
    /**
     * Chooses the left-up candidate from the four possible candidates.
     */
    FixedAlignment["LEFTUP"] = "LEFTUP";
    /**
     * Chooses the right-up candidate from the four possible candidates.
     */
    FixedAlignment["RIGHTUP"] = "RIGHTUP";
    /**
     * Chooses the left-down candidate from the four possible candidates.
     */
    FixedAlignment["LEFTDOWN"] = "LEFTDOWN";
    /**
     * Chooses the right-down candidate from the four possible candidates.
     */
    FixedAlignment["RIGHTDOWN"] = "RIGHTDOWN";
    /**
     * Creates a balanced layout from the four possible candidates.
     */
    FixedAlignment["BALANCED"] = "BALANCED";
})(FixedAlignment = exports.FixedAlignment || (exports.FixedAlignment = {}));
/**
 * Enumerates the strategies for node layering.
 */
var NodeLayering;
(function (NodeLayering) {
    /**
     * This algorithm tries to minimize the length of edges. This is the most computationally intensive algorithm.
     * The number of iterations after which it aborts if it hasn't found a result yet can be set with the Maximal
     * Iterations option.
     */
    NodeLayering["NETWORK_SIMPLEX"] = "NETWORK_SIMPLEX";
    /**
     * A very simple algorithm that distributes nodes along their longest path to a sink node.
     */
    NodeLayering["LONGEST_PATH"] = "LONGEST_PATH";
    /**
     * Distributes the nodes into layers by comparing their positions before the layout algorithm was started.
     * The idea is that the relative horizontal order of nodes as it was before layout was applied is not changed.
     * This of course requires valid positions for all nodes to have been set on the input graph before calling the
     * layout algorithm. The interactive node layering algorithm uses the Interactive Reference Point option to
     * determine which reference point of nodes are used to compare positions.
     */
    NodeLayering["INTERACTIVE"] = "INTERACTIVE";
})(NodeLayering = exports.NodeLayering || (exports.NodeLayering = {}));
/**
 * Enumerates types of node placement.
 */
var NodePlacement;
(function (NodePlacement) {
    /**
     * Minimizes the number of edge bends at the expense of diagram size: diagrams drawn with this algorithm are
     * usually higher than diagrams drawn with other algorithms.
     */
    NodePlacement["BRANDES_KOEPF"] = "BRANDES_KOEPF";
    /**
     * Computes a balanced placement.
     */
    NodePlacement["LINEAR_SEGMENTS"] = "LINEAR_SEGMENTS";
    /**
     * Tries to keep the preset y coordinates of nodes from the original layout. For dummy nodes, a guess is made to infer their coordinates. Requires the other interactive phase implementations to have run as well.
     */
    NodePlacement["INTERACTIVE"] = "INTERACTIVE";
    /**
     * Minimizes the area at the expense of... well, pretty much everything else.
     */
    NodePlacement["SIMPLE"] = "SIMPLE";
})(NodePlacement = exports.NodePlacement || (exports.NodePlacement = {}));
