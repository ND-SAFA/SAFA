import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type {
  SubtreeLink,
  SubtreeMap,
  SetOpacityRequest,
  Project,
} from "@/types";
import { projectModule, subtreeModule } from "@/store";
import { artifactTreeCyPromise, createSubtreeMap } from "@/cytoscape";

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
  private subtreeLinks: SubtreeLink[] = [];

  /**
   * List of nodes currently hidden within subtrees
   */
  private hiddenSubtreeNodes: string[] = [];

  /**
   * List of nodes whose children are currently hidden.
   */
  private collapsedParentNodes: string[] = [];

  /**
   * The amount of child nodes that a node must have greater than or equal to
   * for the node to have its children automatically hidden.
   */
  private autoCollapseSubtreeSize = 5;

  @Action
  /**
   * Recalculates the subtree map of project artifacts and updates store.
   */
  async updateSubtreeMap(): Promise<void> {
    artifactTreeCyPromise.then(async (cy) => {
      const subtreeMap = await createSubtreeMap(cy, projectModule.artifacts);

      this.SET_SUBTREE_MAP(subtreeMap);
    });
  }

  @Action
  /**
   * Resets hidden nodes.
   */
  async resetHiddenNodes(): Promise<void> {
    this.SET_COLLAPSED_PARENT_NODES([]);
    this.SET_HIDDEN_SUBTREE_NODES([]);
    await this.showAllEntities();
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
   * Updates the subtree map, and hides all subtrees greater than the set threshold.
   */
  async initializeProject(project: Project): Promise<void> {
    const artifactIds = project.artifacts.map(({ id }) => id).reverse();
    const childrenPerArtifact = project.traces
      .map(({ targetId }) => targetId)
      .reduce(
        (acc, id) => ({ ...acc, [id]: (acc[id] || 0) + 1 }),
        {} as Record<string, number>
      );

    await subtreeModule.updateSubtreeMap();

    for (const id of artifactIds) {
      if (this.hiddenSubtreeNodes.includes(id)) continue;

      const childCount = childrenPerArtifact[id] || 0;

      if (childCount >= this.autoCollapseSubtreeSize) {
        await this.hideSubtree(id);
      }
    }
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

    for (const childId of childrenInSubtree) {
      const newSubtreeLinks = this.createSubtreeLinks(
        nodesInSubtree,
        rootId,
        childId
      );

      this.SET_SUBTREE_LINKS(newSubtreeLinks);
      this.SET_HIDDEN_SUBTREE_NODES([
        ...this.hiddenSubtreeNodes,
        ...childrenInSubtree,
      ]);
      this.SET_COLLAPSED_PARENT_NODES([...this.collapsedParentNodes, rootId]);
      await this.setProjectEntityVisibility({
        targetArtifactIds: this.hiddenSubtreeNodes,
        visible: false,
      });
    }
  }

  @Action
  /**
   * Un-hides the given artifact's subtree if hidden.
   *
   * @param rootId Id of artifact whose subtree showed by un-hidden.
   */
  async showSubtree(rootId: string): Promise<void> {
    this.SET_SUBTREE_LINKS(
      this.subtreeLinks.filter((link) => link.rootNode !== rootId)
    );

    const subtreeNodes = this.getSubtreeByArtifactId(rootId);

    this.SET_HIDDEN_SUBTREE_NODES(
      this.hiddenSubtreeNodes.filter((n) => !subtreeNodes.includes(n))
    );
    this.SET_COLLAPSED_PARENT_NODES(
      this.collapsedParentNodes.filter((n) => n !== rootId)
    );
    await this.setProjectEntityVisibility({
      targetArtifactIds: subtreeNodes,
      visible: true,
    });
  }

  @Action
  /**
   * Set the visibility of nodes and edges related to given list of artifact names.
   * A node is related if it represents one of the target artifacts.
   * An edge is related if either source or target is an artifact in target
   * list.
   *
   * @param request Contains the target set of artifact names and whether they should be visible.
   */
  async setProjectEntityVisibility(request: SetOpacityRequest): Promise<void> {
    const { targetArtifactIds, visible } = request;
    const display = visible ? "element" : "none";

    artifactTreeCyPromise.then((cy) => {
      cy.nodes()
        .filter((n) => targetArtifactIds.includes(n.data().id))
        .style({ display });

      cy.edges()
        .filter(
          (e) =>
            targetArtifactIds.includes(e.target().data().id) ||
            targetArtifactIds.includes(e.source().data().id)
        )
        .style({ display });
    });
  }

  @Action
  /**
   * Shows all nodes and edges.
   */
  async showAllEntities(): Promise<void> {
    artifactTreeCyPromise.then((cy) => {
      cy.nodes().style({ display: "element" });
      cy.edges().style({ display: "element" });
    });
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
  SET_SUBTREE_LINKS(subtreeLinks: SubtreeLink[]): void {
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
  get getSubtreeLinks(): SubtreeLink[] {
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
  ) => SubtreeLink[] {
    return (nodesInSubtree: string[], rootId: string, childId: string) => {
      const traceLinks = projectModule.traceLinks;

      const subtreeLinkCreator: (f: boolean) => SubtreeLink[] = (
        isIncoming: boolean
      ) => {
        return traceLinks
          .filter((link) => {
            const value = isIncoming ? link.targetId : link.sourceId;
            const oppoValue = isIncoming ? link.sourceId : link.targetId;
            return value === childId && !nodesInSubtree.includes(oppoValue);
          })
          .map((link) => {
            const base: SubtreeLink = {
              ...link,
              type: "SUBTREE",
              rootNode: rootId,
            };

            return isIncoming
              ? { ...base, target: rootId }
              : { ...base, source: rootId };
          });
      };

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
      if (!this.collapsedParentNodes.includes(parentId)) {
        return [];
      }

      const childNodes = this.getSubtreeByArtifactId(parentId);
      const hiddenNodes = this.getHiddenSubtreeIds;

      return childNodes.filter((id) => hiddenNodes.includes(id));
    };
  }
}
