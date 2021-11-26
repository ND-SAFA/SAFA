import { Artifact, CyPromise, CytoCore } from "@/types";
import { SingularElementArgument, EdgeCollection } from "cytoscape";
import { SubtreeMap } from "@/types/store/artifact-selection";

/**
 * Computes the subtree map of given artifacts.
 *
 * @return Promise containing SubtreeMap
 */
export function createSubtreeMap(
  cyPromise: CyPromise,
  artifacts: Artifact[]
): Promise<SubtreeMap> {
  return cyPromise.then((cy) => {
    const subtreeMap = {}; //hash table of previously computed subtrees
    return artifacts
      .map((artifact) => ({
        [artifact.name]: getSubtree(cy, artifact.name, subtreeMap),
      }))
      .reduce((acc, cur) => ({ ...acc, ...cur }), {});
  });
}

/**
 * Returns list of children names for artifact specified.
 * @param cy The cytoscape instance to operate on
 * @param artifactName The name of the root artifacts whose subtree is being
 * calculated.
 * @param subtreeMap Map of previously calculated subtrees used to look up
 * previous calculations.
 */
function getSubtree(
  cy: CytoCore,
  artifactName: string,
  subtreeMap: SubtreeMap
): string[] {
  if (artifactName in subtreeMap) {
    return subtreeMap[artifactName];
  }
  let currentSubtree: string[] = [];
  for (const childName of getChildren(cy, artifactName)) {
    if (!(childName in subtreeMap)) {
      subtreeMap[childName] = getSubtree(cy, childName, subtreeMap);
    }
    const childSubtree = subtreeMap[childName].concat([childName]);
    const newSubtreeArtifacts = childSubtree.filter(
      (t) => !currentSubtree.includes(t)
    );
    currentSubtree = currentSubtree.concat(newSubtreeArtifacts);
  }
  return currentSubtree;
}

/**
 * Returns list of artifact names corresponding to children of artifact.
 * @param cytoCore
 * @param artifactName
 */
function getChildren(cytoCore: CytoCore, artifactName: string): string[] {
  const nodeEdges = cytoCore.edges(`edge[source="${artifactName}"]`);
  const children = nodeEdges.targets();
  return children.map((child) => child.data().id);
}

/**
 * Returns the top most parent from all elements in the cytoscape object.
 * Starting at the node with most edges, its parent is followed until no
 * more exist. If a loop is encountered, then the first repeated node is returned.
 *
 * @param cyPromise - A promise returning cytoscape whose root node is returned.
 * @param currentNode - Defines where we are in the tree during recursion.
 * @param traversedNodes - A list of all traversed node IDs to avoid loops.
 */
export async function getRootNode(
  cyPromise: Promise<CytoCore>,
  currentNode?: SingularElementArgument,
  traversedNodes: string[] = []
): Promise<SingularElementArgument> {
  const cyCore = await cyPromise;

  if (cyCore.nodes().length === 0) {
    throw Error("Root node does not exist because no nodes are in view.");
  }

  if (currentNode === undefined) {
    currentNode = getMostConnectedNode(cyCore);
  }

  // Avoid getting stuck in cycles.
  if (traversedNodes.includes(currentNode.id())) {
    return currentNode;
  } else {
    traversedNodes.push(currentNode.id());
  }

  const edgesOutOfNode: EdgeCollection = cyCore
    .edges()
    .filter((e) => e.target() === currentNode);

  if (edgesOutOfNode.length === 0) {
    return currentNode;
  } else {
    return getRootNode(cyPromise, edgesOutOfNode[0].source(), traversedNodes);
  }
}

/**
 * Returns the node in given Cytoscape instance with the most number of
 * connected edges.
 * @param cyCore
 */
function getMostConnectedNode(cyCore: CytoCore): SingularElementArgument {
  const counts: Record<string, number> = {};
  cyCore.edges().forEach((edge) => {
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
  let maxName = cyCore.nodes().first().data().name;
  for (const [name, count] of Object.entries(counts)) {
    if (count > max) {
      max = count;
      maxName = name;
    }
  }

  return cyCore
    .nodes()
    .filter((n) => n.data().id === maxName)
    .first();
}
