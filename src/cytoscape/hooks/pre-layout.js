"use strict";
exports.__esModule = true;
exports.DefaultPreLayoutHooks = exports.applyOpacityToGeneratedLinks = exports.applyNodeHtml = void 0;
var styles_1 = require("@/cytoscape/styles");
/**
 * Applies HTML overlays to the graph nodes.
 *
 * @param cy - The cy instance.
 */
var applyNodeHtml = function (cy) {
    cy.nodeHtmlLabel([styles_1.artifactHtml]);
};
exports.applyNodeHtml = applyNodeHtml;
/**
 * Applies style changes to graph links.
 *
 * @param cy - The cy instance.
 */
var applyOpacityToGeneratedLinks = function (cy) {
    cy.edges(styles_1.GENERATED_LINK_SELECTOR).forEach(function (edge) {
        var score = edge.data().score;
        edge.style({
            width: score * styles_1.GENERATED_TRACE_MAX_WIDTH
        });
    });
};
exports.applyOpacityToGeneratedLinks = applyOpacityToGeneratedLinks;
/**
 * Validates and stores elements in layout objects applying custom styling as needed.
 */
exports.DefaultPreLayoutHooks = [
    exports.applyNodeHtml,
    exports.applyOpacityToGeneratedLinks,
];
