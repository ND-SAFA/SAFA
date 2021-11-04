import type { Artifact } from "@/types/domain/artifact";
import { cyPromise, getArtifactSubTree } from "@/cytoscape/cytoscape";
import { appModule, artifactSelectionModule, projectModule } from "@/store";
import { Module, VuexModule, Action, Mutation } from "vuex-module-decorators";
import type { CytoCore } from "@/types/cytoscape";
import { PanelType } from "@/types/store";
import {
  ANIMATION_DURATION,
  DEFAULT_ZOOM,
  ZOOM_INCREMENT,
} from "@/cytoscape/styles/config/graph";
import GraphLayout from "@/cytoscape/layout/graph-layout";
import { areArraysEqual } from "@/util";
import {
  isInSubtree,
  doesNotContainType,
  isRelatedToArtifacts,
} from "@/cytoscape/filters/graph-filters";

@Module({ namespaced: true, name: "viewport" })
export default class ViewportModule extends VuexModule {
  currentCenteringCollection: undefined | string[] = undefined;

  @Action
  viewArtifactSubtree(artifact: Artifact): Promise<void> {
    return getArtifactSubTree(artifact).then(async (artifactsInSubtree) => {
      appModule.openPanel(PanelType.left);
      artifactSelectionModule.selectArtifact(artifact);
      await artifactSelectionModule.filterGraph({
        type: "subtree",
        artifactsInSubtree,
      });
    });
  }

  @Action
  repositionSelectedSubtree(): Promise<void> {
    return cyPromise.then((cy: CytoCore) => {
      const artifactsInSubTree: string[] =
        artifactSelectionModule.getSelectedSubtree;
      if (!cy.animated()) {
        this.centerOnArtifacts(artifactsInSubTree);
      }
    });
  }

  @Action
  setGraphLayout(): Promise<void> {
    return cyPromise.then((cyCore: CytoCore) => {
      const layout = new GraphLayout();
      layout.createLayout(cyCore);
      cyCore.zoom(DEFAULT_ZOOM);
    });
  }

  @Action
  onZoomOut(): Promise<void> {
    return cyPromise.then((cyCore: CytoCore) => {
      cyCore.zoom(cyCore.zoom() - ZOOM_INCREMENT);
    });
  }

  @Action
  onZoomIn(): Promise<void> {
    return cyPromise.then((cyCore: CytoCore) => {
      cyCore.zoom(cyCore.zoom() + ZOOM_INCREMENT);
    });
  }

  @Action
  /**
   * Moves the viewport such that given set of artifacts is in the middle of the viewport.
   * If not artifacts are given, the entire collection of nodes is centered.
   * Request is ignored if current animation is in progress to center the same collection of artifacts.
   * @param cyCore - The Cytoscape singleton
   * @param artifacts - The artifacts whose average point will be centered.
   * @returns
   */
  centerOnArtifacts(artifacts: string[]): void {
    cyPromise.then((cyCore: CytoCore) => {
      if (cyCore.animated()) {
        if (
          this.currentCenteringCollection !== undefined &&
          areArraysEqual(this.currentCenteringCollection, artifacts)
        ) {
          console.warn("collection is already being rendered: ", artifacts);
          return;
        } else {
          cyCore.stop(false, false); // clear queue | jump to end
        }
      }
      this.SET_CURRENT_COLLECTION(artifacts);
      const collection =
        artifacts.length === 0
          ? cyCore.nodes()
          : cyCore.nodes().filter((n) => artifacts.includes(n.data().id));

      cyCore.animate({
        center: { eles: collection },
        duration: ANIMATION_DURATION,
        complete: () => this.SET_CURRENT_COLLECTION(undefined),
      });
    });
  }

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
  SET_CURRENT_COLLECTION(p: string[] | undefined): void {
    this.currentCenteringCollection = p;
  }
}
