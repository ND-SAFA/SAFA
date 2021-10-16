/**
 * Extracted from https://developer.mozilla.org/en-US/docs/Web/CSS/cursor
 */
export enum CSSCursor {
  AUTO = "auto", //The UA will determine the cursor to display based on the current context. E.g., equivalent to text when hovering text.
  POINTER = "pointer", // The cursor is a pointer that indicates a link. Typically an image of a pointing hand.
  CONTEXT_MENU = "context-menu", // A context menu is available.
  HELP = "help", // Help information is available.
  WAIT = "wait", // The program is busy, and the user can't interact with the interface (in contrast to progress). Sometimes an image of an hourglass or a watch.
  CELL = "cell", //The table cell or set of cells can be selected.
  CROSSHAR = "crosshair", // Cross cursor, often used to indicate selection in a bitmap.
  NOT_ALLOWED = "not-allowed",
  ZOOM_IN = "zoom-in", //Something can be zoomed (magnified) in or out.
  ZOOM_OUT = "zoom-out",
  GRAB = "grab", // Something can be grabbed (dragged to be moved).
  TEXT = "text", //The text can be selected. Typically the shape of an I-beam.
}
