import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import {
  ArtifactModel,
  ProjectModel,
  SubtreeLinkModel,
  SubtreeMap,
  TraceLinkModel,
} from "@/types";
import {
  createPhantomLinks,
  createSubtreeMap,
  getMatchingChildren,
} from "@/util";
import { cyDisplayAll, cySetDisplay } from "@/cytoscape";
import artifactStore from "./useArtifacts";
import traceStore from "./useTraces";

/**
 * This module keeps track of the tree of artifacts.
 */
export const useSubtree = defineStore("subtrees", {
  state: () => ({
    /**
     * A map containing root artifact names as keys and children names are values.
     */
    subtreeMap: {} as SubtreeMap,
    /**
     * List of phantom links used when hiding subtrees.
     */
    subtreeLinks: [] as SubtreeLinkModel[],
    /**
     * List of artifact ids currently hidden within subtrees.
     */
    hiddenSubtreeNodes: [] as string[],
    /**
     * List of artifact ids whose children are currently hidden.
     */
    collapsedParentNodes: [] as string[],
  }),
  getters: {},
  actions: {
    /**
     * Recalculates the subtree map of project artifacts and updates store.
     *
     * @param artifacts - The artifacts to create the subtree for.
     * @param traces - The traces to create the subtree for.
     */
    updateSubtreeMap(
      artifacts: ArtifactModel[] = artifactStore.allArtifacts,
      traces: TraceLinkModel[] = traceStore.allTraces
    ): void {
      this.subtreeMap = createSubtreeMap(artifacts, traces);
    },
    /**
     * Resets all hidden nodes.
     */
    resetHiddenNodes(): void {
      this.collapsedParentNodes = [];
      this.hiddenSubtreeNodes = [];
      cyDisplayAll();
    },
    /**
     * Updates the subtree map.
     */
    initializeProject(project: ProjectModel): void {
      this.updateSubtreeMap(project.artifacts, project.traces);
    },
    /**
     * Creates phantom links between the given artifacts.
     *
     * @param nodesInSubtree - The nodes in the subtree to create links for.
     * @param rootId - The root node id.
     * @param childId - The child node id.
     * @return A list of phantom links.
     */
    createSubtreeLinks(
      nodesInSubtree: string[],
      rootId: string,
      childId: string
    ): SubtreeLinkModel[] {
      const traces = traceStore.currentTraces;
      const subtreeLinkIds = this.subtreeLinks.map(
        ({ traceLinkId }) => traceLinkId
      );
      const subtreeLinkCreator = createPhantomLinks(
        traces,
        subtreeLinkIds,
        nodesInSubtree,
        rootId,
        childId
      );

      const incomingPhantom = subtreeLinkCreator(true);
      const outgoingPhantom = subtreeLinkCreator(false);

      return [...this.subtreeLinks, ...incomingPhantom, ...outgoingPhantom];
    },
    /**
     * Hides the given artifact's subtree and add replaces child links with
     * phantom links. For any child link leaving a node, a phantom link is added
     * between the target and root node. Similarly, for any linking incoming to a
     * child node, a phantom link is added from the link source to the root node.
     *
     * @param rootId - The Id of the root artifact whose subtree is being hidden.
     */
    async hideSubtree(rootId: string): Promise<void> {
      const childrenInSubtree = this.subtreeMap[rootId];
      const nodesInSubtree = [...childrenInSubtree, rootId];
      const visibleChildren = childrenInSubtree.filter(
        (id) => !this.hiddenSubtreeNodes.includes(id)
      );

      this.$patch({
        subtreeLinks: childrenInSubtree
          .map((childId) =>
            this.createSubtreeLinks(nodesInSubtree, rootId, childId)
          )
          .reduce((acc, cur) => [...acc, ...cur], this.subtreeLinks),
        hiddenSubtreeNodes: [...this.hiddenSubtreeNodes, ...visibleChildren],
        collapsedParentNodes: [...this.collapsedParentNodes, rootId],
      });

      cySetDisplay(visibleChildren, false);
    },
    /**
     * Un-hides the given artifact's subtree if hidden.
     *
     * @param rootId - The Id of artifact whose subtree showed by un-hidden.
     */
    async showSubtree(rootId: string): Promise<void> {
      const subtreeNodes = this.subtreeMap[rootId];
      const hiddenSubtreeNodes = this.hiddenSubtreeNodes.filter(
        (n) => !subtreeNodes.includes(n)
      );

      this.$patch({
        hiddenSubtreeNodes,
        collapsedParentNodes: this.collapsedParentNodes.filter(
          (n) => n !== rootId
        ),
        subtreeLinks: this.subtreeLinks.filter(
          (link) =>
            link.rootNode !== rootId &&
            // Make sure that phantom links created by other parent nodes are removed.
            (hiddenSubtreeNodes.includes(link.sourceId) ||
              hiddenSubtreeNodes.includes(link.targetId))
        ),
      });

      cySetDisplay(subtreeNodes, true);
    },
    /**
     * Temporarily removes all hidden nodes, runs the callback, then restores the hidden nodes.
     *
     * @param cb - The callback run in between.
     */
    async restoreHiddenNodesAfter(cb: () => Promise<void>): Promise<void> {
      const collapsedParents = this.collapsedParentNodes;

      await this.resetHiddenNodes();
      await cb();

      for (const id of collapsedParents) {
        if (this.hiddenSubtreeNodes.includes(id)) continue;

        await this.hideSubtree(id);
      }
    },
    /**
     * Finds the id of all child artifacts that are hidden.
     *
     * @param parentId - The parent artifact to search under.
     * @return The ids of all hidden child artifacts.
     */
    getHiddenChildren(parentId: string): string[] {
      return this.subtreeMap[parentId].filter((id) =>
        this.hiddenSubtreeNodes.includes(id)
      );
    },
    /**
     * Finds all children of the parent nodes matching the child types.
     *
     * @param parentIds - The artifact ids to search under.
     * @param childTypes - The child artifact types to filter children by.
     * @return The ids of all matching children.
     */
    getMatchingChildren(parentIds: string[], childTypes: string[]): string[] {
      return getMatchingChildren(
        parentIds,
        childTypes,
        (id) => this.subtreeMap[id],
        artifactStore.getArtifactById
      );
    },
  },
});

export default useSubtree(pinia);
