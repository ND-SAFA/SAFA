import { Module, VuexModule, Action, Mutation } from "vuex-module-decorators";
import {
  artifactTreeCyPromise,
  getArtifactSubTree,
  getRootNode,
  isInSubtree,
  doesNotContainType,
  isRelatedToArtifacts,
  ANIMATION_DURATION,
  CENTER_GRAPH_PADDING,
  DEFAULT_ZOOM,
  ZOOM_INCREMENT,
  ArtifactGraphLayout,
  TimGraphLayout,
  timTreeCyPromise,
} from "@/cytoscape";
import type { CytoCore, Artifact, CyPromise, LayoutPayload } from "@/types";
import { areArraysEqual } from "@/util";
import { artifactSelectionModule, projectModule } from "@/store";

@Module({ namespaced: true, name: "viewport" })
/**
 * THis module manages the viewport of the artifact graph.
 */
export default class ViewportModule extends VuexModule {
  /**
   * A collection of artifact names currently centered on.
   */
  private currentCenteringCollection?: string[];

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
  async viewArtifactSubtree(
    artifact: Artifact,
    cyPromise: CyPromise = artifactTreeCyPromise
  ): Promise<void> {
    const artifactsInSubtree = await getArtifactSubTree(cyPromise, artifact);
    artifactSelectionModule.selectArtifact(artifact);

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
    const cy = await artifactTreeCyPromise;
    const artifactsInSubTree = artifactSelectionModule.getSelectedSubtree;

    if (!cy.animated()) {
      await this.centerOnArtifacts(artifactsInSubTree);
    }
  }

  @Action
  /**
   * Resets the graph layout of the artifact tree
   */
  async setArtifactTreeLayout(): Promise<void> {
    const layout = new ArtifactGraphLayout();
    const payload = { layout, cyPromise: artifactTreeCyPromise };
    await this.setGraphLayout(payload);
  }

  @Action
  /**
   * Resets the graph layout of the tim tree graph.
   */
  async setTimTreeLayout(): Promise<void> {
    const layout = new TimGraphLayout();
    const payload = { layout, cyPromise: timTreeCyPromise };
    await this.setGraphLayout(payload);
  }

  @Action
  /**
   * Resets the graph layout.
   */
  async setGraphLayout(layoutPayload: LayoutPayload): Promise<void> {
    console.log("GRAPH PAYLOAD: ", layoutPayload);
    const cy = await layoutPayload.cyPromise;
    layoutPayload.layout.createLayout(cy);
    cy.zoom(DEFAULT_ZOOM);
  }

  @Action
  /**
   * Zooms the viewport out.
   */
  async onZoomOut(
    cyPromise: Promise<CytoCore> = artifactTreeCyPromise
  ): Promise<void> {
    const cy = await cyPromise;

    cy.zoom(cy.zoom() - ZOOM_INCREMENT);
    cy.center(cy.nodes());
  }

  @Action
  /**
   * Zooms the viewport in.
   *
   * @param cyPromise - A promise returning cytoscape instance to zoom on.
   */
  async onZoomIn(
    cyPromise: Promise<CytoCore> = artifactTreeCyPromise
  ): Promise<void> {
    const cy = await cyPromise;

    cy.zoom(cy.zoom() + ZOOM_INCREMENT);
    cy.center(cy.nodes());
  }

  @Action
  /**
   * Moves the viewport such that top most parent is centered at default zoom.
   * @param cyPromise - A promise returning a cytoscape instance whose root
   * node is calculated relative to.
   */
  async centerOnRootNode(
    cyPromise: Promise<CytoCore> = artifactTreeCyPromise
  ): Promise<void> {
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
   * @param artifacts - The artifacts whose average point will be centered.
   */
  async centerOnArtifacts(artifacts: string[]): Promise<void> {
    const cy = await artifactTreeCyPromise;

    if (cy.animated()) {
      if (
        this.currentCenteringCollection !== undefined &&
        areArraysEqual(this.currentCenteringCollection, artifacts)
      ) {
        console.warn("collection is already being rendered: ", artifacts);
        return;
      } else {
        cy.stop(false, false);
      }
    }

    this.SET_CURRENT_COLLECTION(artifacts);

    const collection =
      artifacts.length === 0
        ? cy.nodes()
        : cy.nodes().filter((n) => artifacts.includes(n.data().id));
    if (collection.length > 1) {
      cy.animate({
        fit: { eles: collection, padding: CENTER_GRAPH_PADDING },
        duration: ANIMATION_DURATION,
        complete: () => this.SET_CURRENT_COLLECTION(undefined),
      });
    } else {
      cy.animate({
        zoom: DEFAULT_ZOOM,
        center: { eles: collection },
        duration: ANIMATION_DURATION,
        complete: () => this.SET_CURRENT_COLLECTION(undefined),
      });
    }
  }

  /**
   * @return nodes in the current viewport.
   */
  get getNodesInView(): Promise<string[]> {
    const subtree = artifactSelectionModule.getSelectedSubtree;
    const ignoreTypes = artifactSelectionModule.getIgnoreTypes;
    const artifacts: Artifact[] = projectModule.getArtifacts;
    const unselectedNodeOpacity =
      artifactSelectionModule.getUnselectedNodeOpacity;

    const filteredArtifactIds = artifacts
      .filter(
        (a) => isInSubtree(subtree, a) && doesNotContainType(ignoreTypes, a)
      )
      .map((a) => a.name);

    return new Promise((resolve) => {
      artifactTreeCyPromise.then((cyCore: CytoCore) => {
        cyCore.elements().style("opacity", 1);
        cyCore
          .elements()
          .filter((e) => !isRelatedToArtifacts(filteredArtifactIds, e))
          .style("opacity", unselectedNodeOpacity);
        resolve(filteredArtifactIds);
      });
    });
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
}
