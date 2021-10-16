import { NodeCollection } from "cytoscape";
import { CytoCore } from "@/types/cytoscape";
import { DefaultKlayLayout } from "@/cytoscape/layout/klay-layout-settings";
import {
  AutoMoveEventHandlers,
  DefaultAutoMoveEventHandlers,
} from "@/cytoscape/automove";
import {
  CytoEventHandlers,
  DefaultCytoEventHandlers,
} from "@/cytoscape/events/cyto-events";
import IGraphLayout from "@/types/cytoscape/igraph-layout";
import { DefaultPreLayoutHooks } from "@/cytoscape/hooks/pre-layout";
import { DefaultPostLayoutHooks } from "@/cytoscape/hooks/post-layout";
import { KlayLayoutSettings, LayoutHook } from "@/types/cytoscape/klay";

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
