import { appModule, projectModule, viewportModule } from "@/store";
import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { Artifact, FilterAction } from "@/types";
import { PanelType } from "@/types";

@Module({ namespaced: true, name: "artifactSelection" })
/**
 * This module defines the currently selected artifact and downstream artifacts associated with it.
 */
export default class ArtifactSelectionModule extends VuexModule {
  /**
   * The currently selected artifact.
   */
  private selectedArtifactId = "";
  /**
   * The currently selected subtree.
   */
  private selectedSubtreeIds: string[] = [];
  /**
   * The opacity of unselected artifact nodes.
   */
  private unselectedNodeOpacity = 0.1;
  /**
   * Types to ignore.
   */
  private ignoreTypes: string[] = [];

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
  async selectArtifact(artifact: Artifact): Promise<void> {
    this.SELECT_ARTIFACT(artifact.id);
    appModule.openPanel(PanelType.left);
    await viewportModule.centerOnArtifacts([artifact.id]);
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

  @Mutation
  /**
   * Sets a subtree of artifacts as selected.
   *
   * @param artifactIds - The artifact subtree to select.
   */
  SET_SELECTED_SUBTREE(artifactIds: string[]): void {
    this.selectedSubtreeIds = artifactIds;
  }

  @Mutation
  /**
   * Adds an artifact type to ignore from selection.
   *
   * @param artifactType - The type to ignore.
   */
  ADD_IGNORE_TYPE(artifactType: string): void {
    this.ignoreTypes.push(artifactType);
  }

  @Mutation
  /**
   * Removes an ignored artifact type.
   *
   * @param artifactType - The type to stop ignoring.
   */
  REMOVE_IGNORE_TYPE(artifactType: string): void {
    this.ignoreTypes = this.ignoreTypes.filter(
      (type: string) => type !== artifactType
    );
  }

  @Mutation
  /**
   * Sets the given artifact as selected.
   *
   * @param artifactId - The name of the artifact to select.
   */
  SELECT_ARTIFACT(artifactId: string): void {
    this.selectedArtifactId = artifactId;
  }

  @Mutation
  /**
   * Unselects any selected artifact and closes the left app panel.
   */
  UNSELECT_ARTIFACT(): void {
    this.selectedArtifactId = "";
  }

  /**
   * @return The currently selected artifact.
   */
  get getSelectedArtifact(): Artifact | undefined {
    if (this.selectedArtifactId !== "") {
      return projectModule.getArtifactById(this.selectedArtifactId);
    }
  }

  /**
   * @return The currently selected artifact subtree.
   */
  get getSelectedSubtreeIds(): string[] {
    return this.selectedSubtreeIds;
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
}
