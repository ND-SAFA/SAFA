"use strict";
exports.__esModule = true;
exports.CSSCursor = void 0;
/**
 * Extracted from: https://developer.mozilla.org/en-US/docs/Web/CSS/cursor
 *
 * Enumerates cursor types.
 */
var CSSCursor;
(function (CSSCursor) {
    /**
     * The UA will determine the cursor to display based on the current context.
     * E.g., equivalent to text when hovering text.
     */
    CSSCursor["AUTO"] = "auto";
    /**
     * The cursor is a pointer that indicates a link. Typically an image of a pointing hand.
     */
    CSSCursor["POINTER"] = "pointer";
    /**
     * A context menu is available.
     */
    CSSCursor["CONTEXT_MENU"] = "context-menu";
    /**
     * Help information is available.
     */
    CSSCursor["HELP"] = "help";
    /**
     * The program is busy, and the user can't interact with the interface (in contrast to progress).
     * Sometimes an image of an hourglass or a watch.
     */
    CSSCursor["WAIT"] = "wait";
    /**
     * The table cell or set of cells can be selected.
     */
    CSSCursor["CELL"] = "cell";
    /**
     * Cross cursor, often used to indicate selection in a bitmap.
     */
    CSSCursor["CROSSHAIR"] = "crosshair";
    /**
     * Clicking here is not allowed.
     */
    CSSCursor["NOT_ALLOWED"] = "not-allowed";
    /**
     * Something can be zoomed in.
     */
    CSSCursor["ZOOM_IN"] = "zoom-in";
    /**
     * Something can be zoomed out.
     */
    CSSCursor["ZOOM_OUT"] = "zoom-out";
    /**
     * Something can be grabbed (dragged to be moved).
     */
    CSSCursor["GRAB"] = "grab";
    /**
     * Something can be grabbed (dragged to be moved).
     */
    CSSCursor["GRABBING"] = "grabbing";
    /**
     * The text can be selected. Typically the shape of an I-beam.
     */
    CSSCursor["TEXT"] = "text";
})(CSSCursor = exports.CSSCursor || (exports.CSSCursor = {}));
