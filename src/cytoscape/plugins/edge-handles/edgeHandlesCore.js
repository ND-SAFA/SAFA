"use strict";
exports.__esModule = true;
exports.disableDrawMode = exports.enableDrawMode = exports.getEdgeHandlesCore = exports.setEdgeHandlesCore = void 0;
var types_1 = require("@/types");
var onComplete_1 = require("@/cytoscape/plugins/edge-handles/onComplete");
var store_1 = require("@/store");
var edgeHandlesCore = undefined;
/**
 * Initializes edge handling.
 *
 * @param cyPromise - The cy instance.
 * @param instance - The edge handles instance.
 */
function setEdgeHandlesCore(cyPromise, instance) {
    edgeHandlesCore = instance;
    return cyPromise.then(function (cy) {
        cy.on(types_1.CytoEvent.EH_COMPLETE, function (event) {
            var args = [];
            for (var _i = 1; _i < arguments.length; _i++) {
                args[_i - 1] = arguments[_i];
            }
            return onComplete_1.onArtifactTreeEdgeComplete(cy, event, args[0], args[1], args[2]);
        });
    });
}
exports.setEdgeHandlesCore = setEdgeHandlesCore;
/**
 * Returns the edge handle core.
 */
function getEdgeHandlesCore() {
    if (edgeHandlesCore === undefined) {
        store_1.logModule.onDevMessage("EdgeHandles has not been instantiated");
    }
    return edgeHandlesCore;
}
exports.getEdgeHandlesCore = getEdgeHandlesCore;
/**
 * Enables edge drawing mode.
 */
function enableDrawMode() {
    var core = getEdgeHandlesCore();
    if (!core)
        return;
    core.enable();
    core.enableDrawMode();
    store_1.appModule.SET_CREATE_LINK_ENABLED(true);
}
exports.enableDrawMode = enableDrawMode;
/**
 * Disables edge drawing mode.
 */
function disableDrawMode() {
    var core = getEdgeHandlesCore();
    if (!core)
        return;
    core.disableDrawMode();
    core.disable();
    store_1.appModule.SET_CREATE_LINK_ENABLED(false);
}
exports.disableDrawMode = disableDrawMode;
