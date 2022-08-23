import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import {
  artifactTreeCyPromise,
  cyCenterOnArtifacts,
  cyIfNotAnimated,
  doesNotContainType,
  isInSubtree,
} from "@/cytoscape";
import { ArtifactModel, FilterAction, PanelType } from "@/types";
import subtreeStore from "../project/useSubtree";
import artifactStore from "../project/useArtifacts";
import appStore from "../core/useApp";

/**
 * Manages selection of parts of the project.
 */
export const useSelection = defineStore("selection", {
  state: () => ({
    /**
     * A collection of artifact ids currently centered on.
     */
    centeredArtifacts: [] as string[],
    /**
     * The currently selected artifact.
     */
    selectedArtifactId: "",
    /**
     * The currently selected artifact subtree.
     */
    selectedSubtreeIds: [] as string[],
    /**
     * The currently selected group of artifacts.
     */
    selectedGroupIds: [] as string[],
    /**
     * The artifact types to ignore.
     */
    ignoreTypes: [] as string[],
  }),
  getters: {
    /**
     * @return The ids of artifacts that are in the viewport.
     */
    artifactsInView(): string[] {
      const subtree = this.selectedSubtreeIds;
      const ignoreTypes = this.ignoreTypes;

      return artifactStore.currentArtifacts
        .filter(
          (artifact) =>
            isInSubtree(subtree, artifact) &&
            doesNotContainType(ignoreTypes, artifact)
        )
        .map(({ id }) => id);
    },
    /**
     * @return The currently selected artifact.
     */
    selectedArtifact(): ArtifactModel | undefined {
      return artifactStore.getArtifactById(this.selectedArtifactId);
    },
  },
  actions: {
    /**
     * Clears any selected artifact(s) in artifact tree.
     */
    clearSelections(): void {
      this.selectedSubtreeIds = [];
      this.selectedGroupIds = [];
      this.selectedArtifactId = "";
      appStore.closePanel(PanelType.left);
    },
    /**
     * Sets the viewport to the given artifact and its subtree.
     *
     * @param artifactId - The artifact id to select and view.
     */
    viewArtifactSubtree(artifactId: string): void {
      const artifactsInSubtree = [
        ...(subtreeStore.subtreeMap[artifactId] || []),
        artifactId,
      ];

      this.selectArtifact(artifactId);
      this.filterGraph({
        type: "subtree",
        artifactsInSubtree,
      });
    },
    /**
     * Moves the viewport such that given set of artifacts is in the middle of the viewport.
     * If no artifacts are given, the entire collection of nodes is centered.
     *
     * @param artifactIds - The artifacts whose average point will be centered.
     * @param cyPromise - A promise returning an instance of cytoscape.
     */
    centerOnArtifacts(
      artifactIds: string[],
      cyPromise = artifactTreeCyPromise
    ): void {
      cyCenterOnArtifacts(
        this.centeredArtifacts,
        artifactIds,
        (ids) => (this.centeredArtifacts = ids || []),
        cyPromise
      );
    },
    /**
     * Repositions the currently selected subtree of artifacts.
     */
    repositionSelectedSubtree(): void {
      cyIfNotAnimated(() => this.centerOnArtifacts(this.selectedSubtreeIds));
    },
    /**
     * Sets the given artifact as selected.
     *
     * @param artifactId - The artifact to select.
     */
    selectArtifact(artifactId: string): void {
      this.selectedArtifactId = artifactId;

      appStore.openPanel(PanelType.left);
      this.centerOnArtifacts([artifactId]);
    },
    /**
     * Sets the given artifact as selected if it is not already,
     * otherwise clears the current selection.
     *
     * @param artifactId - The artifact to select.
     */
    toggleSelectArtifact(artifactId: string): void {
      if (this.selectedArtifactId === artifactId) {
        this.clearSelections();
      } else {
        this.selectArtifact(artifactId);
      }
    },
    /**
     * Filters the current artifact graph by the given filter type and action.
     *
     * @param filterAction - How to filter the graph.
     */
    filterGraph(filterAction: FilterAction): void {
      if (filterAction.type === "ignore") {
        if (filterAction.action === "add") {
          this.ignoreTypes = [...this.ignoreTypes, filterAction.ignoreType];
        } else if (filterAction.action === "remove") {
          this.ignoreTypes = this.ignoreTypes.filter(
            (type) => type !== filterAction.ignoreType
          );
        }
      } else if (filterAction.type === "subtree") {
        this.selectedSubtreeIds = filterAction.artifactsInSubtree;
        this.repositionSelectedSubtree();
      }
    },
    /**
     * Adds an artifact to the current selection.
     *
     * @param artifactId - The artifact to add.
     */
    addToSelectedGroup(artifactId: string): void {
      this.selectedGroupIds = [...this.selectedGroupIds, artifactId];
    },
    /**
     * Returns whether an artifact is within those selected.
     *
     * @param artifactId - The artifact to check.
     * @return Whether it is selected.
     */
    isArtifactInSelected(artifactId: string): boolean {
      return (
        artifactId === this.selectedArtifactId ||
        this.selectedGroupIds.includes(artifactId)
      );
    },
  },
});

export default useSelection(pinia);
