import { defineStore } from "pinia";

import {
  ArtifactSchema,
  ArtifactTypeSchema,
  FilterAction,
  TraceLinkSchema,
  TraceMatrixSchema,
} from "@/types";
import { LARGE_NODE_COUNT, sanitizeNodeId } from "@/util";
import {
  timStore,
  subtreeStore,
  artifactStore,
  traceStore,
  appStore,
  cyStore,
} from "@/hooks";
import { pinia } from "@/plugins";

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
    selectedArtifactId: "",
    /**
     * The currently selected trace link.
     */
    selectedTraceLinkIds: ["", ""] as [string, string],
    /**
     * The currently selected artifact level.
     */
    selectedArtifactLevelType: "",
    /**
     * The currently selected trace matrix.
     */
    selectedTraceMatrixTypes: ["", ""] as [string, string],
  }),
  getters: {
    /**
     * @return The currently selected artifact.
     */
    selectedArtifact(): ArtifactSchema | undefined {
      return artifactStore.getArtifactById(this.selectedArtifactId);
    },
    /**
     * @return The currently selected trace link.
     */
    selectedTraceLink(): TraceLinkSchema | undefined {
      return traceStore.getTraceLinkByArtifacts(
        this.selectedTraceLinkIds[0],
        this.selectedTraceLinkIds[1]
      );
    },
    /**
     * @return The currently selected artifact level.
     */
    selectedArtifactLevel(): ArtifactTypeSchema | undefined {
      return timStore.getType(this.selectedArtifactLevelType);
    },
    /**
     * @return The currently selected trace matrix.
     */
    selectedTraceMatrix(): TraceMatrixSchema | undefined {
      return timStore.getMatrix(
        this.selectedTraceMatrixTypes[0],
        this.selectedTraceMatrixTypes[1]
      );
    },
    /**
     * @return The ids of artifacts that are in the viewport.
     */
    artifactsInView(): string[] {
      const subtree = this.selectedSubtreeIds;
      const ignoreTypes = this.ignoreTypes;

      const isInSubtree = (id: string) =>
        subtree.length === 0 || subtree.includes(id);
      const doesNotContainType = (type: string) => !ignoreTypes.includes(type);

      return artifactStore.currentArtifacts
        .filter(
          (artifact) =>
            isInSubtree(artifact.id) && doesNotContainType(artifact.type)
        )
        .map(({ id }) => id);
    },
  },
  actions: {
    /**
     * Clears any selected elements in the graph.
     * Each clear is wrapped in an if-statement to help improve performance on large graphs.
     *
     * @param clearFilter - Whether to clear the filter types.
     */
    clearSelections(clearFilter = false): void {
      if (this.ignoreTypes.length > 0) {
        this.ignoreTypes = clearFilter ? [] : this.ignoreTypes;
      }
      if (this.selectedSubtreeIds.length > 0) {
        this.selectedSubtreeIds = [];
      }
      if (this.selectedGroupIds.length > 0) {
        this.selectedGroupIds = [];
      }
      if (this.selectedArtifactId) {
        this.selectedArtifactId = "";
      }
      if (this.selectedTraceLinkIds[0]) {
        this.selectedTraceLinkIds = ["", ""];
      }
      if (this.selectedArtifactLevelType) {
        this.selectedArtifactLevelType = "";
      }
      if (this.selectedTraceMatrixTypes[0]) {
        this.selectedTraceMatrixTypes = ["", ""];
      }
      if (appStore.popups.detailsPanel) {
        appStore.closeSidePanels();
      }
    },
    /**
     * Moves the viewport such that given set of artifacts is in the middle of the viewport.
     * If no artifacts are given, the entire collection of nodes is centered.
     *
     * @param artifactIds - The artifacts whose average point will be centered.
     */
    centerOnArtifacts(artifactIds: string[]): void {
      cyStore.centerOnArtifacts(
        this.centeredArtifacts,
        artifactIds,
        (ids) => (this.centeredArtifacts = ids || [])
      );
    },
    /**
     * Sets the given artifact as selected.
     * To improve performance on large graphs, this function does the following:
     * - Clear selected trace links and nothing else.
     * - Only highlight the related artifacts on smaller graphs.
     *
     * @param artifactId - The artifact to select.
     */
    selectArtifact(artifactId: string): void {
      this.selectedTraceLinkIds = ["", ""];
      this.selectedArtifactId = artifactId;

      if (artifactStore.currentArtifacts.length > LARGE_NODE_COUNT) {
        this.centerOnArtifacts([artifactId]);
      } else {
        this.filterGraph({
          type: "subtree",
          nodeIds: [
            ...(subtreeStore.subtreeMap[artifactId]?.neighbors || []),
            artifactId,
          ],
          centerIds: [artifactId],
        });
      }

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
     * To improve performance on large graphs, this function does the following:
     * - Clear selected artifact and nothing else.
     * - Only highlight the related artifacts on smaller graphs.
     *
     * @param traceLink - The trace link to select.
     */
    selectTraceLink(traceLink: TraceLinkSchema): void {
      const nodeIds: [string, string] = [
        traceLink.sourceId,
        traceLink.targetId,
      ];

      this.selectedArtifactId = "";
      this.selectedTraceLinkIds = nodeIds;

      if (artifactStore.currentArtifacts.length > LARGE_NODE_COUNT) {
        this.centerOnArtifacts(nodeIds);
      } else {
        this.filterGraph({ type: "subtree", nodeIds });
      }

      appStore.openDetailsPanel("displayTrace");
    },
    /**
     * Sets the given artifact level as selected.
     *
     * @param artifactType - The artifact type to select.
     */
    selectArtifactLevel(artifactType: string): void {
      this.clearSelections();
      this.selectedArtifactLevelType = artifactType;
      this.filterGraph({
        type: "subtree",
        nodeIds: [sanitizeNodeId(artifactType)],
      });
      appStore.openDetailsPanel("displayArtifactLevel");
    },
    /**
     * Sets the given trace matrix as selected.
     *
     * @param sourceType - The artifact source type to select.
     * @param targetType - The artifact target type to select.
     */
    selectTraceMatrix(sourceType: string, targetType: string): void {
      const nodeIds = [
        sanitizeNodeId(sourceType),
        sanitizeNodeId(targetType),
      ] as [string, string];

      this.clearSelections();
      this.selectedTraceMatrixTypes = nodeIds;
      this.filterGraph({ type: "subtree", nodeIds });
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
        this.selectedSubtreeIds = filterAction.nodeIds;

        cyStore.ifNotAnimated(() =>
          this.centerOnArtifacts(filterAction.centerIds || filterAction.nodeIds)
        );
      }
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
