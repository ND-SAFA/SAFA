import { Core, LayoutOptions, Layouts, Stylesheet } from "cytoscape";
import {
  AutoMoveOptions,
  AutoMoveRule,
  EdgeHandleCore,
  EdgeHandlersOptions,
  KlayLayoutOptions,
} from "@/types/cytoscape";

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
