import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type { Artifact, FilterAction } from "@/types";
import { PanelType } from "@/types";
import {
  appModule,
  artifactModule,
  artifactSelectionModule,
  logModule,
  viewportModule,
} from "@/store";

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
   * The currently selected group of nodes.
   */
  private selectedGroupIds: string[] = [];
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
   * @param artifactId - The artifact to select.
   */
  selectArtifact(artifactId: string): void {
    this.SELECT_ARTIFACT(artifactId);
    appModule.openPanel(PanelType.left);
    viewportModule.centerOnArtifacts([artifactId]);
  }

  @Action
  /**
   * Sets the given artifact as selected if it is not already,
   * otherwise clears the current selection.
   *
   * @param artifactId - The artifact to select.
   */
  toggleSelectArtifact(artifactId: string): void {
    if (artifactSelectionModule.getSelectedArtifactId === artifactId) {
      artifactSelectionModule.clearSelections();
    } else {
      artifactSelectionModule.selectArtifact(artifactId);
    }
  }

  @Action
  /**
   * Adds the given artifact to the selected group.
   *
   * @param artifactId - The artifact to select.
   */
  addToSelectedGroup(artifactId: string): void {
    this.SELECT_GROUP([...this.selectedGroupIds, artifactId]);
  }

  @Action
  /**
   * Clears any selected artifact(s) in artifact tree.
   */
  clearSelections(): void {
    this.SET_SELECTED_SUBTREE([]);
    this.SELECT_GROUP([]);
    this.UNSELECT_ARTIFACT();
    appModule.closePanel(PanelType.left);
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
   * @param artifactId - The ID of the artifact to select.
   */
  SELECT_ARTIFACT(artifactId: string): void {
    this.selectedArtifactId = artifactId;
  }

  @Mutation
  /**
   * Sets the given artifacts as a selected group.
   *
   * @param artifactIds - The IDs of the group of artifacts to select.
   */
  SELECT_GROUP(artifactIds: string[]): void {
    this.selectedGroupIds = artifactIds;
  }

  @Mutation
  /**
   * Unselects any selected artifact and closes the left app panel.
   */
  UNSELECT_ARTIFACT(): void {
    this.selectedArtifactId = "";
  }

  /**
   * @return The currently selected artifact id.
   */
  get getSelectedArtifactId(): string {
    return this.selectedArtifactId;
  }

  /**
   * @return The currently selected artifact id.
   */
  get getSelectedGroupIds(): string[] {
    return this.selectedGroupIds;
  }

  /**
   * @return Whether there is a currently selected artifact.
   */
  get isArtifactSelected(): boolean {
    return this.selectedArtifactId !== "";
  }

  /**
   * @return The currently selected artifact.
   */
  get getSelectedArtifact(): Artifact | undefined {
    if (this.selectedArtifactId !== "") {
      try {
        return artifactModule.getArtifactById(this.selectedArtifactId);
      } catch (e) {
        logModule.onError(e);
      }
    }
  }

  /**
   * @return The currently selected artifact subtree.
   */
  get getSelectedSubtreeIds(): string[] {
    return this.selectedSubtreeIds;
  }

  /**
   * @return The currently ignored artifact types.
   */
  get getIgnoreTypes(): string[] {
    return this.ignoreTypes;
  }

  /**
   * @return Whether the given artifact id is selected or in the selected group.
   */
  get isArtifactInSelectedGroup(): (id: string) => boolean {
    return (id) => {
      return (
        id === this.selectedArtifactId || this.selectedGroupIds.includes(id)
      );
    };
  }
}
