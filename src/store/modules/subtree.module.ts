import { projectModule } from "@/store";
import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { SubtreeLink } from "@/types";
import type { SubtreeMap } from "@/types/store/artifact-selection";
import { artifactTreeCyPromise, createSubtreeMap } from "@/cytoscape";
import type { SetOpacityRequest } from "@/types/store/subtree";

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

  @Action
  /**
   * Recalculates the subtree map of project artifacts and updates store.
   */
  async updateSubtreeMap(): Promise<void> {
    const cy = await artifactTreeCyPromise;
    const subtreeMap: SubtreeMap = await createSubtreeMap(
      cy,
      projectModule.getArtifacts
    );
    this.SET_SUBTREE_MAP(subtreeMap);
  }

  @Action
  /**
   * Hides the given artifact's subtree and add replaces child links with
   * phantom links. For any child link leaving a node, a phantom link is added
   * between the target and root node. Similarly, for any linking incoming to a
   * child node, a phantom link is added from the link source to the root node.
   *
   * @param rootName Name of the root artifact whose subtree is being hidden.
   */
  async hideSubtree(rootName: string): Promise<void> {
    const childrenInSubtree: string[] = this.getSubtreeByArtifactName(rootName);
    const nodesInSubtree: string[] = childrenInSubtree.concat([rootName]);
    for (const childName of childrenInSubtree) {
      const newSubtreeLinks = this.createSubtreeLinks(
        nodesInSubtree,
        rootName,
        childName
      );
      this.SET_SUBTREE_LINKS(newSubtreeLinks);
      this.SET_HIDDEN_SUBTREE_NODES(
        this.hiddenSubtreeNodes.concat(childrenInSubtree)
      );
      await this.setProjectEntityOpacity({
        targetArtifactNames: this.hiddenSubtreeNodes,
        opacity: 0,
      });
    }
  }

  @Action
  /**
   * Un-hides the given artifact's subtree if hidden.
   *
   * @param rootName The name of artifact whose subtree showed by un-hidden.
   */
  async showSubtree(rootName: string): Promise<void> {
    this.SET_SUBTREE_LINKS(
      this.subtreeLinks.filter((link) => link.rootNode !== rootName)
    );
    const subtreeNodes = this.getSubtreeByArtifactName(rootName);
    this.SET_HIDDEN_SUBTREE_NODES(
      this.hiddenSubtreeNodes.filter((n) => !subtreeNodes.includes(n))
    );
    await this.setProjectEntityOpacity({
      targetArtifactNames: subtreeNodes,
      opacity: 1,
    });
  }

  @Action
  /**
   * Set the opacity of nodes and edges related to given list of artifact names.
   * A node is related if it represents one of the target artifacts.
   * An edge is related if either source or target is an artifact in target
   * list.
   *
   * @param request Contains the target set of artifact names and opacity to
   * set impacted entities to.
   */
  async setProjectEntityOpacity(request: SetOpacityRequest): Promise<void> {
    const { targetArtifactNames, opacity } = request;
    const cy = await artifactTreeCyPromise;
    const targetNodes = cy
      .nodes()
      .filter((n) => targetArtifactNames.includes(n.data().id));
    targetNodes.style({ opacity });
    const targetLinks = cy
      .edges()
      .filter(
        (e) =>
          targetArtifactNames.includes(e.target().data().id) ||
          targetArtifactNames.includes(e.source().data().id)
      );
    targetLinks.style({ opacity });
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

  /**
    * A map between a root node id and it's children.
\   */
  get getSubtreeMap(): SubtreeMap {
    return this.subtreeMap;
  }

  /**
   * @returns the pre-computed artifacts in the subtree of root specified.
   */
  get getSubtreeByArtifactName(): (n: string) => string[] {
    return (artifactName: string) => {
      return this.getSubtreeMap[artifactName] || [];
    };
  }

  /**
   * @returns list of phantom links used for hiding subtrees.
   */
  get getSubtreeLinks(): SubtreeLink[] {
    return this.subtreeLinks;
  }

  /**
   * @returns list of artifact names currently hidden in a subtree
   */
  get getHiddenSubtreeNodes(): string[] {
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
    return (nodesInSubtree: string[], rootName: string, childName: string) => {
      const traceLinks = projectModule.getTraceLinks;
      const subtreeLinkCreator: (f: boolean) => SubtreeLink[] = (
        isIncoming: boolean
      ) => {
        return traceLinks
          .filter((t) => {
            const value = isIncoming ? t.target : t.source;
            const oppoValue = isIncoming ? t.source : t.target;
            return value === childName && !nodesInSubtree.includes(oppoValue);
          })
          .map((t) => {
            const base: SubtreeLink = {
              ...t,
              type: "SUBTREE",
              rootNode: rootName,
            };

            return isIncoming
              ? { ...base, target: rootName }
              : { ...base, source: rootName };
          });
      };
      const incomingPhantom: SubtreeLink[] = subtreeLinkCreator(true);
      const outgoingPhantom: SubtreeLink[] = subtreeLinkCreator(false);
      return this.subtreeLinks.concat(incomingPhantom).concat(outgoingPhantom);
    };
  }

  /**
   * @return The names of all hidden children below the given node.
   */
  get hiddenChildrenForNode(): (name: string) => string[] {
    return (name) => {
      const childNodes = this.getSubtreeByArtifactName(name);
      const hiddenNodes = this.getHiddenSubtreeNodes;

      return childNodes.filter((id) => hiddenNodes.includes(id));
    };
  }
}
