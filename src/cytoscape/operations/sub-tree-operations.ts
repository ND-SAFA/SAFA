import { Artifact, CytoCore, SubtreeMap } from "@/types";
import { SingularElementArgument, EdgeCollection } from "cytoscape";

/**
 * Computes the subtree map of given artifacts.
 *
 * @param cy - The cytoscape instance to operate on.
 * @param artifacts - The current artifacts.
 * @return The computed subtree map.
 */
export function createSubtreeMap(
  cy: CytoCore,
  artifacts: Artifact[]
): SubtreeMap {
  const computedSubtrees = {};
  return artifacts
    .map((artifact) => ({
      [artifact.id]: getSubtree(cy, artifact.id, computedSubtrees),
    }))
    .reduce((acc, cur) => ({ ...acc, ...cur }), {});
}

/**
 * Returns list of children names for artifact specified.
 *
 * @param cy - The cytoscape instance to operate on.
 * @param artifactId - The id of the root artifact whose subtree is being calculated.
 * @param subtreeMapCache - A cache of previously calculated subtrees.
 * @return The child ids in the subtree.
 */
function getSubtree(
  cy: CytoCore,
  artifactId: string,
  subtreeMapCache: SubtreeMap
): string[] {
  let currentSubtree: string[] = [];

  if (artifactId in subtreeMapCache) {
    return subtreeMapCache[artifactId];
  }
  for (const childId of getChildren(cy, artifactId)) {
    if (!(childId in subtreeMapCache)) {
      subtreeMapCache[childId] = getSubtree(cy, childId, subtreeMapCache);
    }

    const childSubtreeIds = [...subtreeMapCache[childId], childId];
    const newSubtreeIds = childSubtreeIds.filter(
      (id) => !currentSubtree.includes(id)
    );

    currentSubtree = [...currentSubtree, ...newSubtreeIds];
  }

  return currentSubtree;
}

/**
 * Returns list of artifact ids corresponding to children of artifact.
 *
 * @param cy - The cytoscape instance to operate on.
 * @param artifactId - The id of the root artifact whose subtree is being calculated.
 * @return The computed child artifact ids.
 */
function getChildren(cy: CytoCore, artifactId: string): string[] {
  const nodeEdges = cy.edges(`edge[source="${artifactId}"]`);
  const children = nodeEdges.targets();

  return children.map((child) => child.data().id);
}

/**
 * Returns the top most parent from all elements in the cytoscape object.
 * Starting at the node with most edges, its parent is followed until no
 * more exist. If a loop is encountered, then the first repeated node is returned.
 *
 * @param cy - The cy instance.
 * @param currentNode - Defines where we are in the tree during recursion.
 * @param traversedNodes - A list of all traversed node IDs to avoid loops.
 * @return The root node.
 */
export async function getRootNode(
  cy: CytoCore,
  currentNode?: SingularElementArgument,
  traversedNodes: string[] = []
): Promise<SingularElementArgument | undefined> {
  if (cy.nodes().length === 0) return;

  if (currentNode === undefined) {
    currentNode = getMostConnectedNode(cy);
  }

  // Avoid getting stuck in cycles.
  if (traversedNodes.includes(currentNode.id())) {
    return currentNode;
  } else {
    traversedNodes.push(currentNode.id());
  }

  const edgesOutOfNode: EdgeCollection = cy
    .edges()
    .filter((e) => e.target() === currentNode);

  if (edgesOutOfNode.length === 0) {
    return currentNode;
  } else {
    return getRootNode(cy, edgesOutOfNode[0].source(), traversedNodes);
  }
}

/**
 * Returns the node in given Cytoscape instance with the most connected edges.
 *
 * @param cy - The cytoscape instance to operate on.
 * @return The found node.
 */
function getMostConnectedNode(cy: CytoCore): SingularElementArgument {
  const counts: Record<string, number> = {};

  cy.edges().forEach((edge) => {
    const sourceName = edge.source().data().id;
    const targetName = edge.target().data().id;
    const increaseCounts = (name: string) => {
      if (name in counts) {
        counts[name]++;
      } else {
        counts[name] = 1;
      }
    };
    increaseCounts(sourceName);
    increaseCounts(targetName);
  });

  let max = -1;
  let maxName = cy.nodes().first().data().name;
  for (const [name, count] of Object.entries(counts)) {
    if (count > max) {
      max = count;
      maxName = name;
    }
  }

  return cy
    .nodes()
    .filter((n) => n.data().id === maxName)
    .first();
}
