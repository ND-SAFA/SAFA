"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
exports.__esModule = true;
exports.ArtifactTreeCytoEvents = void 0;
var core_1 = require("@/types/cytoscape/core");
var store_1 = require("@/store");
var cyto_events_1 = require("@/cytoscape/events/cyto-events");
var cytoscape_1 = require("@/cytoscape");
/**
 * Handlers for mouse events on the artifact tree.
 */
exports.ArtifactTreeCytoEvents = __assign(__assign({}, cyto_events_1.DefaultCytoEvents), { unselectArtifactOnBackgroundClick: {
        events: [core_1.CytoEvent.TAP],
        action: function (cy, event) {
            if (event.target === cy) {
                store_1.artifactSelectionModule.clearSelections();
                cytoscape_1.disableDrawMode();
            }
        }
    }, selectAll: {
        events: [core_1.CytoEvent.BOX_SELECT],
        action: function (cy, event) {
            var artifact = event.target.data();
            store_1.artifactSelectionModule.addToSelectedGroup(artifact.id);
        }
    } });
