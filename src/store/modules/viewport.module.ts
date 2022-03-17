import { Module, VuexModule, Action, Mutation } from "vuex-module-decorators";
import type { CytoCore, Artifact, LayoutPayload, IGraphLayout } from "@/types";
import {
  appModule,
  artifactModule,
  artifactSelectionModule,
  subtreeModule,
} from "@/store";
import {
  artifactTreeCyPromise,
  getRootNode,
  isInSubtree,
  doesNotContainType,
  ArtifactGraphLayout,
  TimGraphLayout,
  timTreeCyPromise,
  cyIfNotAnimated,
  cyCreateLayout,
  cyCenterOnArtifacts,
  cyApplyAutomove,
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

    artifactSelectionModule.selectArtifact(artifact.id);

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

    cyIfNotAnimated(() => this.centerOnArtifacts(artifactsInSubTree));
  }

  @Action
  /**
   * Resets the graph layout of the artifact tree.
   */
  async setArtifactTreeLayout(): Promise<void> {
    const layout = new ArtifactGraphLayout();
    const payload = { layout, cyPromise: artifactTreeCyPromise };

    await this.setGraphLayout(payload);
  }

  @Action({ rawError: true })
  /**
   * Resets the TIM graph back to fit all nodes.
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
    appModule.onLoadStart();

    this.SET_LAYOUT(layoutPayload.layout);
    cyCreateLayout(layoutPayload);

    setTimeout(appModule.onLoadEnd, 200);
  }

  @Action
  /**
   * Moves the viewport such that top most parent is centered at default zoom.
   * @param cyPromise - A promise returning a cytoscape instance whose root
   * node is calculated relative to.
   */
  centerOnRootNode(cyPromise: Promise<CytoCore> = artifactTreeCyPromise): void {
    cyPromise.then((cy) => {
      getRootNode(cy).then((rootNode) => {
        if (!rootNode) return;

        this.centerOnArtifacts([rootNode.data()?.id]);
      });
    });
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
    cyCenterOnArtifacts(
      this.currentCenteringCollection,
      artifactIds,
      (ids) => this.SET_CURRENT_COLLECTION(ids),
      cyPromise
    );
  }

  @Action
  /**
   * Deselects all artifacts.
   */
  deselectArtifacts(): void {
    this.SET_CURRENT_COLLECTION([]);
  }

  @Action
  /**
   * Resets all automove events.
   */
  applyAutomove(): void {
    if (this.currentLayout) {
      cyApplyAutomove(this.currentLayout);
    }
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

    return artifactModule.artifacts
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
