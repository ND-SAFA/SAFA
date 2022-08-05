import {
  KlayLayoutSettings,
  LayoutHook,
  IGraphLayout,
  AutoMoveEventHandlers,
  CytoCore,
  CytoEventHandlers,
} from "@/types";
import { layoutModule } from "@/store";
import { NodeSingular } from "cytoscape";

/**
 * Defines a graph layout.
 */
export default class GraphLayout implements IGraphLayout {
  klaySettings: KlayLayoutSettings | undefined;
  preLayoutHooks: LayoutHook[];
  postLayoutHooks: LayoutHook[];
  autoMoveHandlers: AutoMoveEventHandlers;
  cytoEventHandlers: CytoEventHandlers;

  constructor(
    autoMoveHandlers: AutoMoveEventHandlers,
    cytoEventHandlers: CytoEventHandlers,
    layoutTemplate: KlayLayoutSettings | undefined,
    preLayoutHooks: LayoutHook[],
    postLayoutHooks: LayoutHook[]
  ) {
    this.klaySettings = layoutTemplate;
    this.preLayoutHooks = preLayoutHooks;
    this.postLayoutHooks = postLayoutHooks;
    this.autoMoveHandlers = autoMoveHandlers;
    this.cytoEventHandlers = cytoEventHandlers;
  }

  /**
   * Creates the layout.
   *
   * @param cy - The cy instance.
   */
  createLayout(cy: CytoCore): void {
    this.preLayoutHook(cy);

    if (this.klaySettings) {
      cy.layout({
        name: "klay",
        klay: this.klaySettings,
      }).run();
    } else {
      cy.layout({
        name: "preset",
        fit: true,
        padding: 0,
        positions: (node: NodeSingular | string) => {
          const id = typeof node === "string" ? node : node.data().id;

          return layoutModule.getArtifactPosition(id);
        },
      }).run();
    }

    this.postLayoutHook(cy);
  }

  /**
   * Runs pre-layout hooks.
   *
   * @param cy - The cy instance.
   */
  private preLayoutHook(cy: CytoCore): void {
    for (const preHook of this.preLayoutHooks) {
      preHook(cy, this);
    }
  }

  /**
   * Runs post-layout hooks.
   *
   * @param cy - The cy instance.
   */
  private postLayoutHook(cy: CytoCore): void {
    for (const postHook of this.postLayoutHooks) {
      postHook(cy, this);
    }
  }
}
