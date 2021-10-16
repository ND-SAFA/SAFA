import { Core, LayoutOptions, Layouts } from "cytoscape";
import { AutoMoveOptions, AutoMoveRule } from "@/types/cytoscape/automove";
import { KlayLayoutOptions } from "@/types/cytoscape/klay";
import {
  EdgeHandleCore,
  EdgeHandlersOptions,
} from "@/types/cytoscape/edge-handles";
import { HtmlDefinition } from "@/types/cytoscape/node-html-label";

export interface CytoCore extends Core {
  nodeHtmlLabel: (defs: HtmlDefinition[]) => void;
  automove: (input: string | AutoMoveOptions) => AutoMoveRule;
  contextMenus: (options: unknown) => void;
  layout: (l: LayoutOptions | KlayLayoutOptions) => Layouts;
  edgehandles: (opts: EdgeHandlersOptions) => EdgeHandleCore;
}

/**
 * Extracted from: https://js.cytoscape.org/#events
 */

export enum CytoEvent {
  /**
   * User input device events
   */
  MOUSE_OVER = "mouseover", //when the cursor is put on top of the target
  MOUSE_OUT = "mouseout", // when the cursor is moved off of the target
  RESIZE = "resize", //when the viewport is resized (usually by calling cy.resize(), a window resize, or toggling a class on the Cytoscape.js div)
  /**
   * High level events
   */
  TAP_START = "tapstart", // tap start event (either mousedown or touchstart),
  TAP_DRAG = "tapdrag", //  move event (either touchmove or mousemove)
  TAP_DRAG_OVER = "tapdragover", // over element event (either touchmove or mousemove/mouseover)
  TAP_DRAGOUT = "tapdragout", // off of element event (either touchmove or mousemove/mouseout)
  TAP_END = "tapend", // tap end event (either mouseup or touchend)
  TAP = "tap", // tap event (either click, or touchstart followed by touchend without touchmove)
  TAP_HOLD = "taphold", // tap hold event
  CXT_TAP_START = "cxttapstart", // right-click mousedown or two-finger tapstart
  CXT_TAP_END = "cxttapend", // right-click mouseup or two-finger tapend
  CXT_TAP = "cxttap", // right-click or two-finger tap
  CXT_DRAG = "cxtdrag", // mousemove or two-finger drag after cxttapstart but before cxttapend
  CXT_DRAG_OVER = "cxtdragover", // when going over a node via cxtdrag
  CXT_DRAG_OUT = "cxtdragout", // when going off a node via cxtdrag
  BOX_START = "boxstart", // when starting box selection
  BOX_END = "boxend", // when ending box selection
  BOX_SELECT = "boxselect", // triggered on elements when selected by box selection
  BOX = "box", // triggered on elements when inside the box on boxend

  /**
   * Custom cytoscape events
   */
  ADD = "add", //when an element is added to the graph
  REMOVE = "remove", //when an element is removed from the graph
  MOVE = "move", //when an element is moved w.r.t. topology
  NODES = "nodes", //when the compound parent is changed
  EDGES = "edges", //when the source or target is changed
  SELECT = "select", //when an element is selected
  UNSELECT = "unselect", //when an element is unselected
  TAP_SELECT = "tapselect", //when an element is selected by a tap gesture
  TAP_UNSELECT = "tapunselect", //when an element is unselected by a tap elsewhere
  LOCK = "lock", // when an element is locked
  UNLOCK = "unlock", //when an element is unlocked
  GRAB_ON = "grabon", //when an element is grabbed directly (including only the one node directly under the cursor or the user’s finger)
  GRAB = "grab", //when an element is grabbed (including all elements that would be dragged)
  DRAG = "drag", //when an element is grabbed and then moved
  FREE = "free", //when an element is freed (i.e. let go from being grabbed)
  FREE_ON = "freeon", //when an element is freed directly (including only the one node directly under the cursor or the user’s finger)
  DRAG_FREE = "dragfree", //when an element is freed after being dragged (i.e. grab then drag then free)
  DRAG_FREE_ON = "dragfreeon", //when an element is freed after being dragged directly (i.e. grabon, drag, freeon)
  POSITION = "position", //when an element changes position
  DATA = "data", //when an element’s data is changed
  SCRATCH = "scratch", //when an element’s scratchpad data is changed
  STYLE = "style", //when an element’s style is changed
  BACKGROUND = "background", //when a node’s background image is loaded

  /**
   * EdgeHandle Events
   */
  EH_COMPLETE = "ehcomplete",
}
