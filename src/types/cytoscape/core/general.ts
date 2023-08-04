import {
  Core,
  EventObject,
  LayoutOptions,
  Layouts,
  Stylesheet,
} from "cytoscape";
import {
  AutoMoveOptions,
  AutoMoveRule,
  EdgeHandleCore,
  EdgeHandlersOptions,
  KlayLayoutOptions,
} from "@/types/cytoscape";
import { CytoEvent } from "@/types/cytoscape/core/events";

/**
 * Defines CytoCore, an application specific definition of cytoscape defining
 * interfaces with the plugin made available.
 */
export interface CytoCore extends Core {
  automove(input: string | AutoMoveOptions): AutoMoveRule;
  layout(l: LayoutOptions | KlayLayoutOptions): Layouts;
  edgehandles(opts: EdgeHandlersOptions): EdgeHandleCore;
}

/**
 * Defines a cyto event handler.
 */
export interface CytoEventDefinition {
  events: CytoEvent[];
  selector?: string;
  action: (cy: CytoCore, event: EventObject) => void;
}

/**
 * Defines a collection of cyto event handlers.
 */
export type CytoEventHandlers = Record<string, CytoEventDefinition>;

/**
 * Defines a cyto style sheet.
 */
export type CytoStyleSheet =
  | Stylesheet
  | {
      /**
       * The selector to add this style to.
       */
      selector: string;
      /**
       * The style attributes to add for this selector.
       */
      style: Record<string, unknown>;
    };
