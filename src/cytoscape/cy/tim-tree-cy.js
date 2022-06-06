"use strict";
exports.__esModule = true;
exports.timTreeCyPromise = exports.timTreeResolveCy = void 0;
exports.timTreeResolveCy = null;
/**
 * Returns a promise for the tim tree cy instance.
 * This promise will only resolve when there is a cytoscape graph.
 */
exports.timTreeCyPromise = new Promise(function (resolve) { return (exports.timTreeResolveCy = resolve); });
