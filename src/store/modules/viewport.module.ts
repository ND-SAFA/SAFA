import { Module, VuexModule, Action, Mutation } from "vuex-module-decorators";
import {
  cyPromise,
  getArtifactSubTree,
  getRootNode,
} from "@/cytoscape/cytoscape";
import {
  ANIMATION_DURATION,
  CENTER_GRAPH_PADDING,
  DEFAULT_ZOOM,
  ZOOM_INCREMENT,
} from "@/cytoscape/styles/config/graph";
import GraphLayout from "@/cytoscape/layout/graph-layout";
import {
  isInSubtree,
  doesNotContainType,
  isRelatedToArtifacts,
} from "@/cytoscape/filters/graph-filters";
import type { CytoCore, Artifact } from "@/types";
import { PanelType } from "@/types";
import { areArraysEqual } from "@/util";
import { appModule, artifactSelectionModule, projectModule } from "@/store";

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
  async viewArtifactSubtree(artifact: Artifact): Promise<void> {
    const artifactsInSubtree = await getArtifactSubTree(artifact);
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
    const cy = await cyPromise;
    const artifactsInSubTree = artifactSelectionModule.getSelectedSubtree;

    if (!cy.animated()) {
      await this.centerOnArtifacts(artifactsInSubTree);
    }
  }

  @Action
  /**
   * Resets the graph layout.
   */
  async setGraphLayout(): Promise<void> {
    const cy = await cyPromise;
    const layout = new GraphLayout();

    layout.createLayout(cy);
    cy.zoom(DEFAULT_ZOOM);
  }

  @Action
  /**
   * Zooms the viewport out.
   */
  async onZoomOut(): Promise<void> {
    const cy = await cyPromise;
    cy.zoom(cy.zoom() - ZOOM_INCREMENT);
  }

  @Action
  /**
   * Zooms the viewport in.
   */
  async onZoomIn(): Promise<void> {
    const cy = await cyPromise;
    cy.zoom(cy.zoom() + ZOOM_INCREMENT);
  }

  @Action
  /**
   * Moves the viewport such that top most parent is centered at default zoom.
   *
   */
  async centerOnRootNode(): Promise<void> {
    getRootNode().then((rootNode) =>
      this.centerOnArtifacts([rootNode.data().id])
    );
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
    const cy = await cyPromise;

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
      cyPromise.then((cyCore: CytoCore) => {
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
