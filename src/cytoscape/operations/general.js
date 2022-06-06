"use strict";
exports.__esModule = true;
exports.cyResetTim = exports.cyDisplayAll = exports.cySetDisplay = exports.cyCenterOnArtifacts = exports.cyRemoveAutomove = exports.cyApplyAutomove = exports.cyCreateLayout = exports.cyCenterNodes = exports.cyZoomOut = exports.cyZoomIn = exports.cyZoomReset = exports.cyIfNotAnimated = void 0;
var types_1 = require("@/types");
var cy_1 = require("@/cytoscape/cy");
var styles_1 = require("@/cytoscape/styles");
var store_1 = require("@/store");
var util_1 = require("@/util");
var cytoscape_1 = require("@/cytoscape");
/**
 * Runs the given callback if cy is not animated.
 *
 * @param cb - The callback to run.
 * @param cyPromise - The cy instance.
 */
function cyIfNotAnimated(cb, cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.artifactTreeCyPromise; }
    cyPromise.then(function (cy) {
        if (!cy.animated()) {
            cb();
        }
    });
}
exports.cyIfNotAnimated = cyIfNotAnimated;
/**
 * Resets the zoom level.
 *
 * @param cyPromise - The cy instance.
 */
function cyZoomReset(cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.artifactTreeCyPromise; }
    cyPromise.then(function (cy) {
        cy.zoom(styles_1.DEFAULT_ARTIFACT_TREE_ZOOM);
    });
}
exports.cyZoomReset = cyZoomReset;
/**
 * Zooms in the viewport.
 *
 * @param cyPromise - The cy instance.
 */
function cyZoomIn(cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.artifactTreeCyPromise; }
    cyPromise.then(function (cy) {
        cy.zoom(cy.zoom() + styles_1.ZOOM_INCREMENT);
        cy.center(cy.nodes());
    });
}
exports.cyZoomIn = cyZoomIn;
/**
 * Zooms out the viewport.
 *
 * @param cyPromise - The cy instance.
 */
function cyZoomOut(cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.artifactTreeCyPromise; }
    cyPromise.then(function (cy) {
        cy.zoom(cy.zoom() - styles_1.ZOOM_INCREMENT);
        cy.center(cy.nodes());
    });
}
exports.cyZoomOut = cyZoomOut;
/**
 * Centers the viewport on all graph nodes.
 *
 * @param cyPromise - The cy instance.
 */
function cyCenterNodes(cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.artifactTreeCyPromise; }
    cyPromise.then(function (cy) {
        cy.center(cy.nodes());
    });
}
exports.cyCenterNodes = cyCenterNodes;
/**
 * Creates the given layout.
 *
 * @param layoutPayload - The cy instance and layout.
 */
function cyCreateLayout(layoutPayload) {
    layoutPayload.cyPromise.then(function (cy) {
        layoutPayload.layout.createLayout(cy);
    });
}
exports.cyCreateLayout = cyCreateLayout;
/**
 * Re-applies automove to all nodes.
 *
 * @param layout - The graph layout.
 * @param cyPromise - The cy instance.
 */
function cyApplyAutomove(layout, cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.artifactTreeCyPromise; }
    cyPromise.then(function (cy) {
        cytoscape_1.applyAutoMoveEvents(cy, layout);
    });
}
exports.cyApplyAutomove = cyApplyAutomove;
/**
 * Re-moves automove from all nodes.
 *
 * @param cyPromise - The cy instance.
 */
function cyRemoveAutomove(cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.artifactTreeCyPromise; }
    cyPromise.then(function (cy) {
        cy.automove("destroy");
    });
}
exports.cyRemoveAutomove = cyRemoveAutomove;
/**
 * Moves the viewport such that given set of artifacts is in the middle of the viewport.
 * If no artifacts are given, the entire collection of nodes is centered.
 * Request is ignored if current animation is in progress to center the same collection of artifacts.
 *
 * @param currentCenteringCollection - The current centered artifacts.
 * @param artifactIds - The artifacts whose average point will be centered.
 * @param setCenteredArtifacts - Sets the current centered artifacts.
 * @param cyPromise - A promise returning an instance of cytoscape.
 */
function cyCenterOnArtifacts(currentCenteringCollection, artifactIds, setCenteredArtifacts, cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.artifactTreeCyPromise; }
    cyPromise.then(function (cy) {
        if (cy.animated()) {
            if (currentCenteringCollection !== undefined &&
                util_1.areArraysEqual(currentCenteringCollection, artifactIds)) {
                return store_1.logModule.onDevWarning("Collection is already being rendered: " + artifactIds);
            }
            else {
                cy.stop(false, false);
            }
        }
        setCenteredArtifacts(artifactIds);
        var collection = artifactIds.length === 0
            ? cy.nodes()
            : cy.nodes().filter(function (n) { return artifactIds.includes(n.data().id); });
        if (collection.length > 1) {
            cy.animate({
                fit: { eles: collection, padding: styles_1.CENTER_GRAPH_PADDING },
                duration: styles_1.ANIMATION_DURATION,
                complete: function () { return setCenteredArtifacts(undefined); }
            });
        }
        else {
            cy.animate({
                zoom: styles_1.DEFAULT_ARTIFACT_TREE_ZOOM,
                center: { eles: collection },
                duration: styles_1.ANIMATION_DURATION,
                complete: function () { return setCenteredArtifacts(undefined); }
            });
        }
    });
}
exports.cyCenterOnArtifacts = cyCenterOnArtifacts;
/**
 * Set the visibility of nodes and edges related to given list of artifact names.
 * A node is related if it represents one of the target artifacts.
 * An edge is related if either source or target is an artifact in target
 * list.
 *
 * @param artifactIds - The artifacts to display or hide.
 * @param visible - Whether to display or hide these artifacts.
 * @param cyPromise - The cy instance.
 */
function cySetDisplay(artifactIds, visible, cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.artifactTreeCyPromise; }
    var display = visible ? "element" : "none";
    cyPromise.then(function (cy) {
        cy.nodes()
            .filter(function (n) { return artifactIds.includes(n.data().id); })
            .style({ display: display });
        cy.edges()
            .filter(function (e) {
            return e.data().type !== types_1.InternalTraceType.SUBTREE &&
                artifactIds.includes(e.target().data().id) &&
                artifactIds.includes(e.source().data().id);
        })
            .style({ display: display });
    });
}
exports.cySetDisplay = cySetDisplay;
/**
 * Shows all nodes and edges.
 *
 * @param cyPromise - The cy instance.
 */
function cyDisplayAll(cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.artifactTreeCyPromise; }
    cyPromise.then(function (cy) {
        cy.nodes().style({ display: "element" });
        cy.edges().style({ display: "element" });
    });
}
exports.cyDisplayAll = cyDisplayAll;
/**
 * Centers the viewport on all graph nodes.
 *
 * @param cyPromise - The cy instance.
 */
function cyResetTim(cyPromise) {
    if (cyPromise === void 0) { cyPromise = cy_1.timTreeCyPromise; }
    cyPromise.then(function (cy) {
        cy.zoom(1);
        cy.center(cy.nodes());
    });
}
exports.cyResetTim = cyResetTim;
