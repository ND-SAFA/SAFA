import { defineStore } from "pinia";

import {
  ArtifactSchema,
  FilterAction,
  TimArtifactLevelSchema,
  TimTraceMatrixSchema,
  TraceLinkSchema,
} from "@/types";
import {
  artifactTreeCyPromise,
  cyCenterOnArtifacts,
  cyIfNotAnimated,
  doesNotContainType,
  isInSubtree,
} from "@/cytoscape";
import { pinia } from "@/plugins";
import subtreeStore from "../project/useSubtree";
import artifactStore from "../project/useArtifacts";
import typeOptionsStore from "../project/useTypeOptions";
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

    /**
     * The currently selected artifact.
     */
    selectedArtifact: undefined as ArtifactSchema | undefined,
    /**
     * The currently selected trace link.
     */
    selectedTraceLink: undefined as TraceLinkSchema | undefined,
    /**
     * The currently selected artifact level.
     */
    selectedArtifactLevel: undefined as TimArtifactLevelSchema | undefined,
    /**
     * The currently selected trace matrix.
     */
    selectedTraceMatrix: undefined as TimTraceMatrixSchema | undefined,
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
  },
  actions: {
    /**
     * Clears any selected artifact(s) in artifact tree.
     *
     * @param clearFilter - Whether to clear the filter types.
     */
    clearSelections(clearFilter = false): void {
      this.ignoreTypes = clearFilter ? [] : this.ignoreTypes;
      this.selectedSubtreeIds = [];
      this.selectedGroupIds = [];
      this.selectedArtifact = undefined;
      this.selectedTraceLink = undefined;
      this.selectedArtifactLevel = undefined;
      this.selectedTraceMatrix = undefined;
      appStore.closeSidePanels();
    },
    /**
     * Sets the viewport to the given artifact and its subtree.
     *
     * @param artifactId - The artifact id to select and view.
     */
    viewArtifactSubtree(artifactId: string): void {
      const artifactsInSubtree = [
        ...(subtreeStore.subtreeMap[artifactId].subtree || []),
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
      this.clearSelections();
      this.selectedArtifact = artifactStore.getArtifactById(artifactId);
      this.centerOnArtifacts([artifactId]);
      appStore.openDetailsPanel("displayArtifact");
    },
    /**
     * Sets the given artifact as selected if it is not already,
     * otherwise clears the current selection.
     *
     * @param artifactId - The artifact to select.
     */
    toggleSelectArtifact(artifactId: string): void {
      if (this.selectedArtifact?.id === artifactId) {
        this.clearSelections();
      } else {
        this.selectArtifact(artifactId);
      }
    },
    /**
     * Sets the given trace links as selected.
     *
     * @param traceLink - The trace link to select.
     */
    selectTraceLink(traceLink: TraceLinkSchema): void {
      this.clearSelections();
      this.selectedTraceLink = traceLink;
      this.selectedSubtreeIds = [traceLink.sourceId, traceLink.targetId];
      this.centerOnArtifacts([traceLink.sourceId, traceLink.targetId]);
      appStore.openDetailsPanel("displayTrace");
    },
    /**
     * Sets the given artifact level as selected.
     *
     * @param artifactType - The artifact type to select.
     */
    selectArtifactLevel(artifactType: string): void {
      this.clearSelections();
      this.selectedArtifactLevel =
        typeOptionsStore.getArtifactLevel(artifactType);
      this.centerOnArtifacts([artifactType]);
      appStore.openDetailsPanel("displayArtifactLevel");
    },
    /**
     * Sets the given trace matrix as selected.
     *
     * @param sourceType - The artifact source type to select.
     * @param targetType - The artifact target type to select.
     */
    selectTraceMatrix(sourceType: string, targetType: string): void {
      this.clearSelections();
      this.selectedTraceMatrix = typeOptionsStore.getTraceMatrix(
        sourceType,
        targetType
      );
      this.centerOnArtifacts([sourceType, targetType]);
      appStore.openDetailsPanel("displayTraceMatrix");
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
        artifactId === this.selectedArtifact?.id ||
        this.selectedGroupIds.includes(artifactId)
      );
    },
  },
});

export default useSelection(pinia);
