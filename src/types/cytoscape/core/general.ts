import {
  Core,
  EventObject,
  LayoutOptions,
  Layouts,
  Stylesheet,
} from "cytoscape";
import { ArtifactCytoElementData, TimNodeCytoElementData } from "@/types";
import {
  AutoMoveOptions,
  AutoMoveRule,
  CytoContextMenu,
  EdgeHandleCore,
  EdgeHandlersOptions,
  HtmlDefinition,
  KlayLayoutOptions,
  ContextMenuOptions,
} from "@/types/cytoscape";
import { CytoEvent } from "@/types/cytoscape/core/events";

/**
 * The HtmlDefinitions used with in the application.
 */
type AppHtmlDefinitions = (
  | HtmlDefinition<ArtifactCytoElementData>
  | HtmlDefinition<TimNodeCytoElementData>
)[];

/**
 * Defines CytoCore, an application specific definition of cytoscape defining
 * interfaces with the plugin made available.
 */
export interface CytoCore extends Core {
  nodeHtmlLabel(defs: AppHtmlDefinitions): void;
  automove(input: string | AutoMoveOptions): AutoMoveRule;
  contextMenus(options: ContextMenuOptions | "get"): CytoContextMenu;
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
