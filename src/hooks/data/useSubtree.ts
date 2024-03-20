import { defineStore } from "pinia";

import {
  ProjectSchema,
  SubtreeItemSchema,
  SubtreeMapSchema,
  TraceLinkSchema,
} from "@/types";
import { getMatchingChildren } from "@/util";
import { artifactStore, cyStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This module keeps track of the tree of artifacts.
 */
export const useSubtree = defineStore("subtrees", {
  state: () => ({
    /** A map containing root artifact names as keys and children names are values. */
    subtreeMap: {} as SubtreeMapSchema,
    /** List of artifact ids currently hidden within subtrees. */
    hiddenSubtreeNodes: [] as string[],
    /** List of artifact ids whose children are currently hidden. */
    collapsedParentNodes: [] as string[],
  }),
  getters: {},
  actions: {
    /**
     * Updates the subtree map.
     */
    initializeProject(project: ProjectSchema, preserveHidden?: boolean): void {
      this.subtreeMap = project.subtrees;

      if (preserveHidden) return;

      this.hiddenSubtreeNodes = [];
      this.collapsedParentNodes = [];
    },
    /**
     * Returns the subtree information of an artifact, creating one if none exists.
     *
     * @param artifactId - The artifact to add for.
     *
     */
    getSubtreeItem(artifactId: string): SubtreeItemSchema {
      if (!this.subtreeMap[artifactId]) {
        this.subtreeMap[artifactId] = {
          parents: [],
          children: [],
          subtree: [],
          supertree: [],
          neighbors: [],
        };
      }

      return this.subtreeMap[artifactId];
    },
    /**
     * Returns the subtree of an artifact.
     *
     * @param artifactId - The artifact to get.
     * @return The artifact's subtree.
     */
    getSubtree(artifactId: string): string[] {
      return this.getSubtreeItem(artifactId).subtree;
    },
    /**
     * Returns the parents of an artifact.
     *
     * @param artifactId - The artifact to get.
     * @return The artifact's parents.
     */
    getParents(artifactId: string): string[] {
      return this.getSubtreeItem(artifactId).parents;
    },
    /**
     * Returns the children of an artifact.
     *
     * @param artifactId - The artifact to get.
     * @return The artifact's children.
     */
    getChildren(artifactId: string): string[] {
      return this.getSubtreeItem(artifactId).children;
    },
    /**
     * Returns the combined parents and children of an artifact.
     *
     * @param artifactId - The artifact to get.
     * @return The artifact's children.
     */
    getParentsAndChildren(artifactId: string): string[] {
      return [
        ...this.getSubtreeItem(artifactId).parents,
        ...this.getSubtreeItem(artifactId).children,
      ];
    },
    /**
     * Returns the neighbors of an artifact.
     *
     * @param artifactId - The artifact to get.
     * @return The artifact's children.
     */
    getNeighbors(artifactId: string): string[] {
      return this.getSubtreeItem(artifactId).neighbors;
    },
    /**
     * Returns the relationship between artifacts.
     *
     * @param sourceId - The source artifact's id.
     * @param targetId - The target artifact's id.
     * @return The relationship between these artifacts.
     */
    getRelationship(
      sourceId: string,
      targetId: string
    ): "parent" | "child" | undefined {
      if (this.getParents(sourceId).includes(targetId)) {
        return "parent";
      } else if (this.getChildren(sourceId).includes(targetId)) {
        return "child";
      } else {
        return undefined;
      }
    },
    /**
     * Finds the id of all child artifacts that are hidden.
     * If there are hidden child artifacts, the entire number of hidden subtree artifacts will be returned.
     *
     * @param parentId - The parent artifact to search under.
     * @return The ids of all hidden child artifacts.
     */
    getHiddenChildren(parentId: string): string[] {
      const nodeIsHidden = (id: string) => this.hiddenSubtreeNodes.includes(id);

      return this.getChildren(parentId).filter(nodeIsHidden).length > 0
        ? this.getSubtree(parentId).filter(nodeIsHidden)
        : [];
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
        (id) => this.getSubtree(id),
        artifactStore.getArtifactById
      );
    },
    /**
     * Updates the subtree of an artifact, creating one if none exists.
     *
     * @param artifactId - The artifact to update.
     * @param getUpdatedSubtree - The subtree changes to update with.
     */
    updateSubtree(
      artifactId: string,
      getUpdatedSubtree: (item: SubtreeItemSchema) => Partial<SubtreeItemSchema>
    ): void {
      const existingSubtree = this.getSubtreeItem(artifactId);

      this.subtreeMap[artifactId] = {
        ...existingSubtree,
        ...getUpdatedSubtree(existingSubtree),
      };
    },
    /**
     * Adds a trace to the subtree.
     * Note: Only updates the source and target subtrees.
     *       Does not update the subtree of all neighbors.
     *
     * @param traceLink - The trace link to add the subtree for.
     */
    addTraceSubtree(traceLink: TraceLinkSchema): void {
      this.updateSubtree(traceLink.sourceId, (subtree) => ({
        parents: [...subtree.parents, traceLink.targetId],
        neighbors: [...subtree.neighbors, traceLink.targetId],
        supertree: [...subtree.supertree, traceLink.targetId],
      }));
      this.updateSubtree(traceLink.targetId, (subtree) => ({
        children: [...subtree.children, traceLink.sourceId],
        neighbors: [...subtree.neighbors, traceLink.sourceId],
        subtree: [...subtree.subtree, traceLink.sourceId],
      }));
    },
    /**
     * Deletes a trace from the subtree.
     * Note: Only updates the source and target subtrees.
     *       Does not update the subtree of all neighbors.
     *
     * @param traceLink - The trace link to delete the subtree for.
     */
    deleteTraceSubtree(traceLink: TraceLinkSchema): void {
      this.updateSubtree(traceLink.sourceId, (subtree) => ({
        parents: subtree.parents.filter((id) => id !== traceLink.targetId),
        neighbors: subtree.neighbors.filter((id) => id !== traceLink.targetId),
        supertree: subtree.supertree.filter((id) => id !== traceLink.targetId),
      }));
      this.updateSubtree(traceLink.targetId, (subtree) => ({
        children: subtree.children.filter((id) => id !== traceLink.sourceId),
        neighbors: subtree.neighbors.filter((id) => id !== traceLink.sourceId),
        subtree: subtree.subtree.filter((id) => id !== traceLink.sourceId),
      }));
    },
    /**
     * Resets all hidden nodes.
     */
    resetHiddenNodes(): void {
      if (this.hiddenSubtreeNodes.length > 0) {
        this.collapsedParentNodes = [];
        this.hiddenSubtreeNodes = [];
        cyStore.setDisplay([], true);
      }
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
      const childrenInSubtree = this.getSubtree(rootId);
      const visibleChildren =
        this.hiddenSubtreeNodes.length === 0
          ? childrenInSubtree
          : childrenInSubtree.filter(
              (id) => !this.hiddenSubtreeNodes.includes(id)
            );

      if (visibleChildren.length === 0) return;

      this.$patch({
        hiddenSubtreeNodes: [...this.hiddenSubtreeNodes, ...visibleChildren],
        collapsedParentNodes: [...this.collapsedParentNodes, rootId],
      });

      cyStore.setDisplay(visibleChildren, false);
    },
    /**
     * Hides the subtrees of all children of the given artifact.
     * @param rootId - The Id of the root artifact whose subtree is being hidden.
     */
    hideChildSubtrees(rootId: string): void {
      this.getChildren(rootId).forEach((id) => this.hideSubtree(id));
    },
    /**
     * Hides the subtrees of all leaf nodes in the current document.
     */
    hideLeafSubtrees(): void {
      artifactStore.leaves.forEach((id) => this.hideSubtree(id));
    },
    /**
     * Un-hides the given artifact's subtree if hidden.
     *
     * @param rootId - The Id of artifact whose subtree showed by un-hidden.
     */
    async showSubtree(rootId: string): Promise<void> {
      const subtreeNodes = this.getSubtree(rootId);
      const hiddenSubtreeNodes = this.hiddenSubtreeNodes.filter(
        (id) => !subtreeNodes.includes(id)
      );

      this.$patch({
        hiddenSubtreeNodes,
        collapsedParentNodes: this.collapsedParentNodes.filter(
          (id) => id !== rootId
        ),
      });

      cyStore.setDisplay(subtreeNodes, true);
    },
    /**
     * Temporarily removes all hidden nodes, runs the callback, then restores the hidden nodes.
     *
     * @param cb - The callback run in between.
     */
    async restoreHiddenNodesAfter(cb: () => Promise<void>): Promise<void> {
      const collapsedParents = this.collapsedParentNodes;

      this.resetHiddenNodes();
      await cb();

      for (const id of collapsedParents) {
        if (this.hiddenSubtreeNodes.includes(id)) continue;

        await this.hideSubtree(id);
      }
    },
  },
});

export default useSubtree(pinia);
