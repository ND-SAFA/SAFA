"use strict";
exports.__esModule = true;
exports.ArtifactTreeAutoMoveHandlers = void 0;
var types_1 = require("@/types");
/**
 * Defines a set of triggers-handler pairs for use in the artifact tree graph.
 */
exports.ArtifactTreeAutoMoveHandlers = {
    moveArtifactWithoutSubtree: {
        triggers: [types_1.CytoEvent.CXT_DRAG],
        action: function (node, rule, event) {
            document.body.style.cursor = types_1.CSSCursor.GRAB;
            var nodePosition = event.target.renderedPosition();
            event.target.renderedPosition({
                x: nodePosition.x + event.originalEvent.movementX,
                y: nodePosition.y + event.originalEvent.movementY
            });
        }
    }
};
