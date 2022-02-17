import {
  KlayLayoutSettings,
  LayoutHook,
  IGraphLayout,
  AutoMoveEventHandlers,
  CytoCore,
  CytoEventHandlers,
} from "@/types";

/**
 * Defines a graph layout.
 */
export default class GraphLayout implements IGraphLayout {
  klaySettings: KlayLayoutSettings;
  preLayoutHooks: LayoutHook[];
  postLayoutHooks: LayoutHook[];

  autoMoveHandlers: AutoMoveEventHandlers;
  cytoEventHandlers: CytoEventHandlers;

  constructor(
    autoMoveHandlers: AutoMoveEventHandlers,
    cytoEventHandlers: CytoEventHandlers,
    layoutTemplate: KlayLayoutSettings,
    preLayoutHooks: LayoutHook[],
    postLayoutHooks: LayoutHook[]
  ) {
    this.klaySettings = layoutTemplate;
    this.preLayoutHooks = preLayoutHooks;
    this.postLayoutHooks = postLayoutHooks;
    this.autoMoveHandlers = autoMoveHandlers;
    this.cytoEventHandlers = cytoEventHandlers;
    this.autoMoveHandlers = autoMoveHandlers;
  }

  /**
   * Creates the layout.
   *
   * @param cy - The cy instance.
   */
  createLayout(cy: CytoCore): void {
    this.preLayoutHook(cy);

    cy.layout({
      name: "klay",
      klay: this.klaySettings,
    }).run();

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
