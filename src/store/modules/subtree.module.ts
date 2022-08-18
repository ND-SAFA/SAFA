import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type {
  SubtreeLinkModel,
  SubtreeMap,
  ProjectModel,
  ArtifactModel,
  TraceLinkModel,
} from "@/types";
import { artifactModule, traceModule } from "@/store";
import {
  artifactTreeCyPromise,
  createPhantomLinks,
  createSubtreeMap,
  cyDisplayAll,
  cySetDisplay,
  getMatchingChildren,
} from "@/cytoscape";

@Module({ namespaced: true, name: "subtree" })
/**
 * This module defines the functions used to hide and show subtrees.
 */
export default class SubtreeModule extends VuexModule {
  /**
   * A map containing root artifact names as keys and children names are values.
   */
  private subtreeMap: SubtreeMap = {};

  /**
   * List of phantom links used when hiding subtrees.
   */
  private subtreeLinks: SubtreeLinkModel[] = [];

  /**
   * List of nodes currently hidden within subtrees
   */
  private hiddenSubtreeNodes: string[] = [];

  /**
   * List of nodes whose children are currently hidden.
   */
  private collapsedParentNodes: string[] = [];

  @Action
  /**
   * Recalculates the subtree map of project artifacts and updates store.
   *
   * @param artifacts - The artifacts to create the subtree for.
   */
  async updateSubtreeMap(
    artifacts: ArtifactModel[] = artifactModule.allArtifacts,
    traces: TraceLinkModel[] = traceModule.allTraces
  ): Promise<void> {
    const subtreeMap = await createSubtreeMap(artifacts, traces);

    this.SET_SUBTREE_MAP(subtreeMap);
  }

  @Action
  /**
   * Resets hidden nodes.
   */
  async resetHiddenNodes(): Promise<void> {
    this.SET_COLLAPSED_PARENT_NODES([]);
    this.SET_HIDDEN_SUBTREE_NODES([]);
    cyDisplayAll();
  }

  @Action
  /**
   * Clears all data.
   */
  async clearSubtrees(): Promise<void> {
    this.SET_SUBTREE_MAP({});
    this.SET_SUBTREE_LINKS([]);
    await this.resetHiddenNodes();
  }

  @Action
  /**
   * Temporarily removes all hidden nodes, runs the callback, then restores the hidden nodes.
   */
  async restoreHiddenNodesAfter(cb: () => Promise<void>): Promise<void> {
    const collapsedParents = this.collapsedParentNodes;

    await this.resetHiddenNodes();
    await cb();

    for (const id of collapsedParents) {
      if (this.hiddenSubtreeNodes.includes(id)) continue;

      await this.hideSubtree(id);
    }
  }

  @Action
  /**
   * Updates the subtree map, and hides all subtrees greater than the set threshold.
   */
  async initializeProject(project: ProjectModel): Promise<void> {
    await this.updateSubtreeMap(project.artifacts, project.traces);
  }

  @Action
  /**
   * Hides the given artifact's subtree and add replaces child links with
   * phantom links. For any child link leaving a node, a phantom link is added
   * between the target and root node. Similarly, for any linking incoming to a
   * child node, a phantom link is added from the link source to the root node.
   *
   * @param rootId Id of the root artifact whose subtree is being hidden.
   */
  async hideSubtree(rootId: string): Promise<void> {
    const childrenInSubtree = this.getSubtreeByArtifactId(rootId);
    const nodesInSubtree = [...childrenInSubtree, rootId];
    const visibleChildren = childrenInSubtree.filter(
      (id) => !this.hiddenSubtreeNodes.includes(id)
    );

    for (const childId of childrenInSubtree) {
      const newSubtreeLinks = this.createSubtreeLinks(
        nodesInSubtree,
        rootId,
        childId
      );

      this.SET_SUBTREE_LINKS(newSubtreeLinks);
    }

    this.SET_HIDDEN_SUBTREE_NODES([
      ...this.hiddenSubtreeNodes,
      ...visibleChildren,
    ]);
    this.SET_COLLAPSED_PARENT_NODES([...this.collapsedParentNodes, rootId]);
    cySetDisplay(visibleChildren, false);
  }

  @Action
  /**
   * Un-hides the given artifact's subtree if hidden.
   *
   * @param rootId Id of artifact whose subtree showed by un-hidden.
   */
  async showSubtree(rootId: string): Promise<void> {
    const subtreeNodes = this.getSubtreeByArtifactId(rootId);
    const hiddenNodes = this.hiddenSubtreeNodes.filter(
      (n) => !subtreeNodes.includes(n)
    );

    this.SET_HIDDEN_SUBTREE_NODES(hiddenNodes);
    this.SET_COLLAPSED_PARENT_NODES(
      this.collapsedParentNodes.filter((n) => n !== rootId)
    );
    this.SET_SUBTREE_LINKS(
      this.subtreeLinks.filter(
        (link) =>
          link.rootNode !== rootId &&
          // Make sure that phantom links created by other parent nodes are removed.
          (hiddenNodes.includes(link.sourceId) ||
            hiddenNodes.includes(link.targetId))
      )
    );
    cySetDisplay(subtreeNodes, true);
  }

  @Mutation
  /**
   * Sets current subtree map.
   *
   * @param subtreeMap The map of all the subtrees in project.
   */
  SET_SUBTREE_MAP(subtreeMap: SubtreeMap): void {
    this.subtreeMap = subtreeMap;
  }

  @Mutation
  /**
   * Sets the current subtree links.
   *
   * @param subtreeLinks The list of phantom links used for hiding subtrees.
   */
  SET_SUBTREE_LINKS(subtreeLinks: SubtreeLinkModel[]): void {
    this.subtreeLinks = subtreeLinks;
  }

  @Mutation
  /**
   * Sets the current nodes hidden by subtrees.
   *
   * @param hiddenSubtreeNodes The list of nodes currently being hidden in a subtree.
   */
  SET_HIDDEN_SUBTREE_NODES(hiddenSubtreeNodes: string[]): void {
    this.hiddenSubtreeNodes = hiddenSubtreeNodes;
  }

  @Mutation
  /**
   * Sets the current nodes with hidden subtrees.
   *
   * @param collapsedParentNodes The list of nodes currently having their children hidden.
   */
  SET_COLLAPSED_PARENT_NODES(collapsedParentNodes: string[]): void {
    this.collapsedParentNodes = collapsedParentNodes;
  }

  /**
    * A map between a root node id and it's children.
\   */
  get getSubtreeMap(): SubtreeMap {
    return this.subtreeMap;
  }

  /**
   * @returns the pre-computed artifacts in the subtree of root specified.
   */
  get getSubtreeByArtifactId(): (n: string) => string[] {
    return (artifactId: string) => this.getSubtreeMap[artifactId] || [];
  }

  /**
   * @returns list of phantom links used for hiding subtrees.
   */
  get getSubtreeLinks(): SubtreeLinkModel[] {
    return this.subtreeLinks;
  }

  /**
   * @returns list of artifact ids currently hidden in a subtree.
   */
  get getHiddenSubtreeIds(): string[] {
    return this.hiddenSubtreeNodes;
  }

  /**
   * @returns a constructor for creating phantom links from artifacts.
   */
  get createSubtreeLinks(): (
    n: string[],
    r: string,
    c: string
  ) => SubtreeLinkModel[] {
    return (nodesInSubtree: string[], rootId: string, childId: string) => {
      const traces = traceModule.traces;
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
    };
  }

  /**
   * @return The ids of all hidden children below the given node.
   */
  get getHiddenChildrenByParentId(): (parentId: string) => string[] {
    return (parentId) => {
      const childNodes = this.getSubtreeByArtifactId(parentId);
      const hiddenNodes = this.getHiddenSubtreeIds;

      return childNodes.filter((id) => hiddenNodes.includes(id));
    };
  }

  /**
   * @return The ids of all children under the given parent ids.
   */
  get getMatchingChildren(): (
    parentIds: string[],
    includedChildTypes: string[]
  ) => string[] {
    return (parentIds, includedChildTypes) =>
      getMatchingChildren(
        parentIds,
        includedChildTypes,
        this.getSubtreeByArtifactId,
        artifactModule.getArtifactById
      );
  }

  /**
   * @return Ids of the parent whose children are collapsed.
   * Used for toggling Show/Hide subtree menu items.
   */
  get getCollapsedParentNodes(): string[] {
    return this.collapsedParentNodes;
  }
}
