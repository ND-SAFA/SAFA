import { defineStore } from "pinia";

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
import { pinia } from "@/plugins";
import traceStore from "./useTraces";
import artifactStore from "./useArtifacts";

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
     * Returns the subtree of an artifact.
     *
     * @param artifactId - The artifact to get.
     * @return The artifact's subtree.
     */
    getSubtree(artifactId: string): string[] {
      return this.subtreeMap[artifactId]?.subtree || [];
    },
    /**
     * Returns the parents of an artifact.
     *
     * @param artifactId - The artifact to get.
     * @return The artifact's parents.
     */
    getParents(artifactId: string): string[] {
      return this.subtreeMap[artifactId]?.parents || [];
    },
    /**
     * Returns the children of an artifact.
     *
     * @param artifactId - The artifact to get.
     * @return The artifact's children.
     */
    getChildren(artifactId: string): string[] {
      return this.subtreeMap[artifactId]?.children || [];
    },
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
      const childrenInSubtree = this.getSubtree(rootId);
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
      const subtreeNodes = this.getSubtree(rootId);
      const hiddenSubtreeNodes = this.hiddenSubtreeNodes.filter(
        (id) => !subtreeNodes.includes(id)
      );

      this.$patch({
        hiddenSubtreeNodes,
        collapsedParentNodes: this.collapsedParentNodes.filter(
          (id) => id !== rootId
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
      return this.getSubtree(parentId).filter((id) =>
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
        (id) => this.getSubtree(id),
        artifactStore.getArtifactById
      );
    },
  },
});

export default useSubtree(pinia);
