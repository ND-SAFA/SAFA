import { appModule, projectModule, viewportModule } from "@/store";
import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { Artifact, CytoCore, FilterAction } from "@/types";
import { PanelType } from "@/types";
import { SubtreeMap } from "@/types/store/artifact-selection";
import { artifactTreeCyPromise, createSubtreeMap } from "@/cytoscape";

@Module({ namespaced: true, name: "artifactSelection" })
/**
 * This module defines the currently selected artifact and downstream artifacts associated with it.
 */
export default class ArtifactSelectionModule extends VuexModule {
  /**
   * The currently selected artifact.
   */
  private selectedArtifact?: Artifact = undefined;
  /**
   * The currently selected subtree.
   */
  private selectedSubtree: string[] = [];
  /**
   * The opacity of unselected artifact nodes.
   */
  private unselectedNodeOpacity = 0.1;
  /**
   * Types to ignore.
   */
  private ignoreTypes: string[] = [];

  /**
   * A map containing root artifact names as keys and children names are values.
   */
  private subtreeMap: SubtreeMap = {};

  @Action
  /**
   * Filters the current artifact graph by the given filter type and action.
   *
   * @param filterAction - How to filter the graph.
   */
  async filterGraph(filterAction: FilterAction): Promise<void> {
    switch (filterAction.type) {
      case "ignore":
        switch (filterAction.action) {
          case "add":
            return this.ADD_IGNORE_TYPE(filterAction.ignoreType);
          case "remove":
            return this.REMOVE_IGNORE_TYPE(filterAction.ignoreType);
        }
        break;
      case "subtree":
        this.SET_SELECTED_SUBTREE(filterAction.artifactsInSubtree);
        await viewportModule.repositionSelectedSubtree();
    }
  }

  @Action
  /**
   * Sets the given artifact as selected.
   *
   * @param artifact - The artifact to select.
   */
  selectArtifact(artifact: Artifact): void {
    this.SELECT_ARTIFACT(artifact);
    appModule.openPanel(PanelType.left);
    viewportModule.centerOnArtifacts([artifact.name]).then();
  }

  @Action
  /**
   * Unselects any selected artifact and closes the left app panel.
   */
  unselectArtifact(): void {
    this.UNSELECT_ARTIFACT();
    appModule.closePanel(PanelType.left);
  }

  @Action
  /**
   * Clears any selected artifact(s) in artifact tree.
   */
  clearSelections(): void {
    this.unselectArtifact();
    this.SET_SELECTED_SUBTREE([]);
  }

  @Action
  /**
   * Recalculates the subtree map of project artifacts and updates store.
   */
  async updateSubtreeMap(): Promise<void> {
    const cy = await artifactTreeCyPromise;
    const subtreeMap: SubtreeMap = await createSubtreeMap(
      cy,
      projectModule.getArtifacts
    );
    this.SET_SUBTREE_MAP(subtreeMap);
  }

  @Action
  /**
   * Hides the given artifact's subtree
   */
  hideSubtree(artifactName: string): void {
    console.log("SUBTREE:", this.getSubtreeByArtifactName(artifactName));
  }

  @Action
  /**
   * Un-hides the given artifact's subtree if hidden.
   */
  showSubtree(artifactName: string): void {
    console.log("SUBTREE:", this.getSubtreeByArtifactName(artifactName));
  }

  @Mutation
  /**
   * Sets a subtree of artifacts as selected.
   * @param artifacts - The artifact subtree to select.
   */
  SET_SELECTED_SUBTREE(artifacts: string[]): void {
    this.selectedSubtree = artifacts;
  }

  @Mutation
  /**
   * Adds an artifact type to ignore from selection.
   *
   * @param artifactTypeKey - The type to ignore.
   */
  ADD_IGNORE_TYPE(artifactTypeKey: string): void {
    this.ignoreTypes.push(artifactTypeKey);
  }

  @Mutation
  /**
   * Removes an ignored artifact type.
   *
   * @param artifactTypeKey - The type to stop ignoring.
   */
  REMOVE_IGNORE_TYPE(artifactTypeKey: string): void {
    this.ignoreTypes = this.ignoreTypes.filter(
      (at: string) => at !== artifactTypeKey
    );
  }

  @Mutation
  /**
   * Sets the given artifact as selected.
   *
   * @param artifact - The artifact to select.
   */
  SELECT_ARTIFACT(artifact: Artifact): void {
    this.selectedArtifact = artifact;
  }

  @Mutation
  /**
   * Unselects any selected artifact and closes the left app panel.
   */
  UNSELECT_ARTIFACT(): void {
    this.selectedArtifact = undefined;
  }

  @Mutation
  /**
   * Sets current subtree map.
   */
  SET_SUBTREE_MAP(subtreeMap: SubtreeMap): void {
    this.subtreeMap = subtreeMap;
  }

  /**
   * @return The currently selected artifact.
   */
  get getSelectedArtifact(): Artifact | undefined {
    return this.selectedArtifact;
  }

  /**
   * @return The currently selected artifact subtree.
   */
  get getSelectedSubtree(): string[] {
    return this.selectedSubtree;
  }

  /**
   * @return The node opacity for unselected artifacts.
   */
  get getUnselectedNodeOpacity(): number {
    return this.unselectedNodeOpacity;
  }

  /**
   * @return The currently ignored artifact types.
   */
  get getIgnoreTypes(): string[] {
    return this.ignoreTypes;
  }

  /**
    * A map between a root node id and it's children.
\   */
  get getSubtreeMap(): SubtreeMap {
    return this.subtreeMap;
  }

  /**
   * Returns the pre-computed artifacts in the subtree of root specified.
   */
  get getSubtreeByArtifactName(): (n: string) => string[] {
    return (artifactName: string) => {
      return this.getSubtreeMap[artifactName];
    };
  }
}
