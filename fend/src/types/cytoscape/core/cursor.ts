/**
 * Extracted from: https://developer.mozilla.org/en-US/docs/Web/CSS/cursor
 *
 * Enumerates cursor types.
 */
export enum CSSCursor {
  /**
   * The UA will determine the cursor to display based on the current context.
   * E.g., equivalent to text when hovering text.
   */
  AUTO = "auto",
  /**
   * The cursor is a pointer that indicates a link. Typically an image of a pointing hand.
   */
  POINTER = "pointer",
  /**
   * A context menu is available.
   */
  CONTEXT_MENU = "context-menu",
  /**
   * Help information is available.
   */
  HELP = "help",
  /**
   * The program is busy, and the user can't interact with the interface (in contrast to progress).
   * Sometimes an image of an hourglass or a watch.
   */
  WAIT = "wait",
  /**
   * The table cell or set of cells can be selected.
   */
  CELL = "cell",
  /**
   * Cross cursor, often used to indicate selection in a bitmap.
   */
  CROSSHAIR = "crosshair",
  /**
   * Clicking here is not allowed.
   */
  NOT_ALLOWED = "not-allowed",
  /**
   * Something can be zoomed in.
   */
  ZOOM_IN = "zoom-in",
  /**
   * Something can be zoomed out.
   */
  ZOOM_OUT = "zoom-out",
  /**
   * Something can be grabbed (dragged to be moved).
   */
  GRAB = "grab",
  /**
   * Something can be grabbed (dragged to be moved).
   */
  GRABBING = "grabbing",
  /**
   * The text can be selected. Typically the shape of an I-beam.
   */
  TEXT = "text",
}
