import { NodeCollection } from "cytoscape";
import { DefaultKlayLayout } from "@/cytoscape/layout";
import { ArtifactTreeAutoMoveHandlers } from "@/cytoscape/automove";
import { DefaultCytoEventHandlers } from "@/cytoscape/events";
import {
  DefaultPostLayoutHooks,
  DefaultPreLayoutHooks,
} from "@/cytoscape/hooks";
import {
  KlayLayoutSettings,
  LayoutHook,
  IGraphLayout,
  AutoMoveEventHandlers,
  CytoCore,
  CytoEventHandlers,
} from "@/types";

export default class ArtifactTreeGraphLayout implements IGraphLayout {
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
    autoMoveHandlers: AutoMoveEventHandlers = ArtifactTreeAutoMoveHandlers,
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
