"use strict";
exports.__esModule = true;
exports.CytoEvent = void 0;
/**
 * Enumerates types of cyto events.
 *
 * Extracted from: https://js.cytoscape.org/#events
 */
var CytoEvent;
(function (CytoEvent) {
    /**
     * # User input device events.
     */
    /**
     * When the cursor is put on top of the target.
     */
    CytoEvent["MOUSE_OVER"] = "mouseover";
    /**
     * When the cursor is moved off of the target.
     */
    CytoEvent["MOUSE_OUT"] = "mouseout";
    /**
     * When the viewport is resized (usually by calling cy.resize(),
     * a window resize, or toggling a class on the Cytoscape.js div).
     */
    CytoEvent["RESIZE"] = "resize";
    /**
     * # High level events.
     */
    /**
     * Tap start event (either mousedown or touchstart).
     */
    CytoEvent["TAP_START"] = "tapstart";
    /**
     * Move event (either touchmove or mousemove).
     */
    CytoEvent["TAP_DRAG"] = "tapdrag";
    /**
     * Over element event (either touchmove or mousemove/mouseover).
     */
    CytoEvent["TAP_DRAG_OVER"] = "tapdragover";
    /**
     * Off of element event (either touchmove or mousemove/mouseout).
     */
    CytoEvent["TAP_DRAGOUT"] = "tapdragout";
    /**
     * Tap end event (either mouseup or touchend).
     */
    CytoEvent["TAP_END"] = "tapend";
    /**
     * Tap event (either click, or touchstart followed by touchend without touchmove).
     */
    CytoEvent["TAP"] = "tap";
    /**
     * Tap hold event.
     */
    CytoEvent["TAP_HOLD"] = "taphold";
    /**
     * Right-click mousedown or two-finger tapstart.
     */
    CytoEvent["CXT_TAP_START"] = "cxttapstart";
    /**
     * Right-click mouseup or two-finger tapend.
     */
    CytoEvent["CXT_TAP_END"] = "cxttapend";
    /**
     * Right-click or two-finger tap.
     */
    CytoEvent["CXT_TAP"] = "cxttap";
    /**
     * Mousemove or two-finger drag after cxttapstart but before cxttapend.
     */
    CytoEvent["CXT_DRAG"] = "cxtdrag";
    /**
     * When going over a node via cxtdrag.
     */
    CytoEvent["CXT_DRAG_OVER"] = "cxtdragover";
    /**
     * When going off a node via cxtdrag.
     */
    CytoEvent["CXT_DRAG_OUT"] = "cxtdragout";
    /**
     * When starting box selection.
     */
    CytoEvent["BOX_START"] = "boxstart";
    /**
     * When ending box selection.
     */
    CytoEvent["BOX_END"] = "boxend";
    /**
     * Triggered on elements when selected by box selection.
     */
    CytoEvent["BOX_SELECT"] = "boxselect";
    /**
     * Triggered on elements when inside the box on boxend.
     */
    CytoEvent["BOX"] = "box";
    /**
     * # Custom cytoscape events.
     */
    /**
     * When an element is added to the graph.
     */
    CytoEvent["ADD"] = "add";
    /**
     * When an element is removed from the graph.
     */
    CytoEvent["REMOVE"] = "remove";
    /**
     * When an element is moved w.r.t. topology.
     */
    CytoEvent["MOVE"] = "move";
    /**
     * When the compound parent is changed.
     */
    CytoEvent["NODES"] = "nodes";
    /**
     * When the source or target is changed.
     */
    CytoEvent["EDGES"] = "edges";
    /**
     * When an element is selected.
     */
    CytoEvent["SELECT"] = "select";
    /**
     * When an element is unselected.
     */
    CytoEvent["UNSELECT"] = "unselect";
    /**
     * When an element is selected by a tap gesture.
     */
    CytoEvent["TAP_SELECT"] = "tapselect";
    /**
     * When an element is unselected by a tap elsewhere.
     */
    CytoEvent["TAP_UNSELECT"] = "tapunselect";
    /**
     * When an element is locked.
     */
    CytoEvent["LOCK"] = "lock";
    /**
     * When an element is unlocked.
     */
    CytoEvent["UNLOCK"] = "unlock";
    /**
     * When an element is grabbed directly (including only the one node directly under the cursor or the user’s finger).
     */
    CytoEvent["GRAB_ON"] = "grabon";
    /**
     * When an element is grabbed (including all elements that would be dragged).
     */
    CytoEvent["GRAB"] = "grab";
    /**
     * When an element is grabbed and then moved.
     */
    CytoEvent["DRAG"] = "drag";
    /**
     * When an element is freed (i.e. let go from being grabbed).
     */
    CytoEvent["FREE"] = "free";
    /**
     * When an element is freed directly (including only the one node directly under the cursor or the user’s finger).
     */
    CytoEvent["FREE_ON"] = "freeon";
    /**
     * When an element is freed after being dragged (i.e. grab then drag then free).
     */
    CytoEvent["DRAG_FREE"] = "dragfree";
    /**
     * When an element is freed after being dragged directly (i.e. grabon, drag, freeon).
     */
    CytoEvent["DRAG_FREE_ON"] = "dragfreeon";
    /**
     * When an element changes position.
     */
    CytoEvent["POSITION"] = "position";
    /**
     * When an element’s data is changed.
     */
    CytoEvent["DATA"] = "data";
    /**
     * When an element’s scratchpad data is changed.
     */
    CytoEvent["SCRATCH"] = "scratch";
    /**
     * When an element’s style is changed.
     */
    CytoEvent["STYLE"] = "style";
    /**
     * When a node’s background image is loaded.
     */
    CytoEvent["BACKGROUND"] = "background";
    /**
     * # Edge Handle Events.
     */
    CytoEvent["EH_COMPLETE"] = "ehcomplete";
})(CytoEvent = exports.CytoEvent || (exports.CytoEvent = {}));
