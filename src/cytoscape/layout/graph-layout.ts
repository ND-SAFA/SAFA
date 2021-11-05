import { NodeCollection } from "cytoscape";
import { DefaultKlayLayout } from "@/cytoscape/layout/klay-layout-settings";
import { DefaultAutoMoveEventHandlers } from "@/cytoscape/automove";
import { DefaultCytoEventHandlers } from "@/cytoscape/events/cyto-events";
import { DefaultPreLayoutHooks } from "@/cytoscape/hooks/pre-layout";
import { DefaultPostLayoutHooks } from "@/cytoscape/hooks/post-layout";
import {
  KlayLayoutSettings,
  LayoutHook,
  IGraphLayout,
  AutoMoveEventHandlers,
  CytoCore,
  CytoEventHandlers,
} from "@/types";

export default class GraphLayout implements IGraphLayout {
  klaySettings: KlayLayoutSettings;
  preLayoutHooks: LayoutHook[];
  postLayoutHooks: LayoutHook[];

  autoMoveHandlers: AutoMoveEventHandlers;
  cytoEventHandlers: CytoEventHandlers;

  peerNodes?: NodeCollection;
  temporaryEdges?: NodeCollection;
  packageNodes?: NodeCollection;
  ancestorNodes?: NodeCollection;
  codeNodes?: NodeCollection;
  peerElements?: NodeCollection;

  constructor(
    autoMoveHandlers: AutoMoveEventHandlers = DefaultAutoMoveEventHandlers,
    cytoEventHandlers: CytoEventHandlers = DefaultCytoEventHandlers,
    layoutTemplate: KlayLayoutSettings = DefaultKlayLayout,
    preLayoutHooks: LayoutHook[] = DefaultPreLayoutHooks,
    postLayoutHooks: LayoutHook[] = DefaultPostLayoutHooks
  ) {
    this.klaySettings = layoutTemplate;
    this.preLayoutHooks = preLayoutHooks;
    this.postLayoutHooks = postLayoutHooks;
    this.autoMoveHandlers = autoMoveHandlers;
    this.cytoEventHandlers = cytoEventHandlers;
    this.autoMoveHandlers = autoMoveHandlers;
  }

  createLayout(cy: CytoCore): void {
    this.preLayoutHook(cy);
    cy.layout({
      name: "klay",
      klay: this.klaySettings,
    }).run();
    this.postLayoutHook(cy);
  }

  preLayoutHook(cy: CytoCore): void {
    for (const preHook of this.preLayoutHooks) {
      preHook(cy, this);
    }
  }

  postLayoutHook(cy: CytoCore): void {
    for (const postHook of this.postLayoutHooks) {
      postHook(cy, this);
    }
  }
}
