import { Module, VuexModule, Action, Mutation } from "vuex-module-decorators";
import type { CytoCore, Artifact, LayoutPayload, IGraphLayout } from "@/types";
import { areArraysEqual } from "@/util";
import {
  logModule,
  artifactSelectionModule,
  projectModule,
  subtreeModule,
  viewportModule,
  appModule,
} from "@/store";
import {
  artifactTreeCyPromise,
  getRootNode,
  isInSubtree,
  doesNotContainType,
  ANIMATION_DURATION,
  CENTER_GRAPH_PADDING,
  DEFAULT_ARTIFACT_TREE_ZOOM,
  ZOOM_INCREMENT,
  ArtifactGraphLayout,
  TimGraphLayout,
  timTreeCyPromise,
} from "@/cytoscape";

@Module({ namespaced: true, name: "viewport" })
/**
 * THis module manages the viewport of the artifact graph.
 */
export default class ViewportModule extends VuexModule {
  /**
   * A collection of artifact ids currently centered on.
   */
  private currentCenteringCollection?: string[];
  /**
   * The current graph layout
   */
  private layout?: IGraphLayout;

  @Action
  /**
   * Sets the viewport to the given artifact and its subtree.
   *
   * 1. Opens the left app panel.
   * 2. Selects the given artifact.
   * 3. Filters the artifact graph to only artifacts in this artifact's subtree.
   *
   * @param artifact - The artifact to select and view.
   */
  async viewArtifactSubtree(artifact: Artifact): Promise<void> {
    const artifactsInSubtree = [
      ...subtreeModule.getSubtreeByArtifactId(artifact.id),
      artifact.id,
    ];

    await artifactSelectionModule.selectArtifact(artifact.id);

    await artifactSelectionModule.filterGraph({
      type: "subtree",
      artifactsInSubtree,
    });
  }

  @Action
  /**
   * Repositions the currently selected subtree of artifacts.
   */
  async repositionSelectedSubtree(): Promise<void> {
    const artifactsInSubTree = artifactSelectionModule.getSelectedSubtreeIds;

    artifactTreeCyPromise.then((cy) => {
      if (!cy.animated()) {
        this.centerOnArtifacts(artifactsInSubTree);
      }
    });
  }

  @Action
  /**
   * Resets the graph layout of the artifact tree.
   */
  async setArtifactTreeLayout(): Promise<void> {
    const layout = new ArtifactGraphLayout();
    const payload = { layout, cyPromise: artifactTreeCyPromise };

    await this.setGraphLayout(payload);

    artifactTreeCyPromise.then((cy) => {
      cy.zoom(DEFAULT_ARTIFACT_TREE_ZOOM);
    });
  }

  @Action({ rawError: true })
  /**
   * Resets the TIM graph back to fit all nodes.
   */
  async setTimTreeLayout(): Promise<void> {
    const layout = new TimGraphLayout();
    const payload = { layout, cyPromise: timTreeCyPromise };

    await viewportModule.setGraphLayout(payload);
    appModule.SET_IS_LOADING(true);

    timTreeCyPromise.then((cy) => {
      setTimeout(() => {
        cy.animate({
          center: { eles: cy.nodes() },
          duration: ANIMATION_DURATION,
          complete: () => appModule.SET_IS_LOADING(false),
        });
      }, 250);
    });
  }

  @Action
  /**
   * Resets the graph layout.
   */
  async setGraphLayout(layoutPayload: LayoutPayload): Promise<void> {
    this.SET_LAYOUT(layoutPayload.layout);

    layoutPayload.cyPromise.then((cy) => {
      layoutPayload.layout.createLayout(cy);
    });
  }

  @Action
  /**
   * Zooms the viewport out.
   */
  onZoomOut(cyPromise: Promise<CytoCore> = artifactTreeCyPromise): void {
    cyPromise.then((cy) => {
      cy.zoom(cy.zoom() - ZOOM_INCREMENT);
      cy.center(cy.nodes());
    });
  }

  @Action
  /**
   * Zooms the viewport in.
   *
   * @param cyPromise - A promise returning cytoscape instance to zoom on.
   */
  onZoomIn(cyPromise: Promise<CytoCore> = artifactTreeCyPromise): void {
    cyPromise.then((cy) => {
      cy.zoom(cy.zoom() + ZOOM_INCREMENT);
      cy.center(cy.nodes());
    });
  }

  @Action
  /**
   * Moves the viewport such that top most parent is centered at default zoom.
   * @param cyPromise - A promise returning a cytoscape instance whose root
   * node is calculated relative to.
   */
  centerOnRootNode(cyPromise: Promise<CytoCore> = artifactTreeCyPromise): void {
    getRootNode(cyPromise)
      .then((rootNode) => this.centerOnArtifacts([rootNode.data()?.id]))
      .catch((e) => console.warn(e.message));
  }

  @Action
  /**
   * Moves the viewport such that given set of artifacts is in the middle of the viewport.
   * If no artifacts are given, the entire collection of nodes is centered.
   * Request is ignored if current animation is in progress to center the same collection of artifacts.
   *
   * @param artifactIds - The artifacts whose average point will be centered.
   * @param cyPromise - A promise returning an instance of cytoscape.
   */
  centerOnArtifacts(
    artifactIds: string[],
    cyPromise = artifactTreeCyPromise
  ): void {
    cyPromise.then((cy) => {
      if (cy.animated()) {
        if (
          this.currentCenteringCollection !== undefined &&
          areArraysEqual(this.currentCenteringCollection, artifactIds)
        ) {
          return logModule.onDevWarning(
            `Collection is already being rendered: ${artifactIds}`
          );
        } else {
          cy.stop(false, false);
        }
      }

      this.SET_CURRENT_COLLECTION(artifactIds);

      const collection =
        artifactIds.length === 0
          ? cy.nodes()
          : cy.nodes().filter((n) => artifactIds.includes(n.data().id));

      if (collection.length > 1) {
        cy.animate({
          fit: { eles: collection, padding: CENTER_GRAPH_PADDING },
          duration: ANIMATION_DURATION,
          complete: () => this.SET_CURRENT_COLLECTION(undefined),
        });
      } else {
        cy.animate({
          zoom: DEFAULT_ARTIFACT_TREE_ZOOM,
          center: { eles: collection },
          duration: ANIMATION_DURATION,
          complete: () => this.SET_CURRENT_COLLECTION(undefined),
        });
      }
    });
  }

  @Action
  /**
   * Deselects all artifacts.
   */
  deselectArtifacts(): void {
    this.SET_CURRENT_COLLECTION([]);
  }

  @Mutation
  /**
   * Sets a new layout.
   *
   * @param layout - The new layout to set.
   */
  SET_LAYOUT(layout: IGraphLayout): void {
    this.layout = layout;
  }

  @Mutation
  /**
   * Sets a new centered collection of artifacts.
   *
   * @param centeringCollection - The new collection to set.
   */
  SET_CURRENT_COLLECTION(centeringCollection?: string[]): void {
    this.currentCenteringCollection = centeringCollection;
  }

  /**
   * @return artifact ids of those in viewport.
   */
  get getNodesInView(): string[] {
    const subtree = artifactSelectionModule.getSelectedSubtreeIds;
    const ignoreTypes = artifactSelectionModule.getIgnoreTypes;
    const artifacts = projectModule.artifacts;

    return artifacts
      .filter(
        (a) => isInSubtree(subtree, a) && doesNotContainType(ignoreTypes, a)
      )
      .map((a) => a.id);
  }

  /**
   * @return The currently centered nodes.
   */
  get currentCenteredNodes(): string[] {
    return this.currentCenteringCollection || [];
  }

  /**
   * @return The current layout.
   */
  get currentLayout(): IGraphLayout | undefined {
    return this.layout;
  }
}
