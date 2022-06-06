"use strict";
exports.__esModule = true;
exports.DefaultCytoEvents = void 0;
var types_1 = require("@/types");
/**
 * Handlers for mouse events on the graph.
 */
exports.DefaultCytoEvents = {
    mouseOverCursor: {
        events: [types_1.CytoEvent.MOUSE_OVER],
        selector: "node",
        action: function () {
            document.body.style.cursor = types_1.CSSCursor.POINTER;
        }
    },
    mouseOutCursor: {
        events: [types_1.CytoEvent.MOUSE_OUT],
        selector: "node",
        action: function () {
            document.body.style.cursor = types_1.CSSCursor.AUTO;
        }
    },
    setDragCursor: {
        events: [types_1.CytoEvent.DRAG],
        selector: "node",
        action: function () {
            document.body.style.cursor = types_1.CSSCursor.GRABBING;
        }
    },
    setDragFreeCursor: {
        events: [types_1.CytoEvent.DRAG_FREE, types_1.CytoEvent.FREE],
        selector: "node",
        action: function () {
            document.body.style.cursor = types_1.CSSCursor.AUTO;
        }
    }
};
