"use strict";
exports.__esModule = true;
exports.artifactTreeCyPromise = exports.artifactTreeResolveCy = void 0;
exports.artifactTreeResolveCy = null;
/**
 * Returns a promise for the artifact tree cy instance.
 * This promise will only resolve when there is a cytoscape graph.
 */
exports.artifactTreeCyPromise = new Promise(function (resolve) { return (exports.artifactTreeResolveCy = resolve); });
