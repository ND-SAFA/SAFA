import { CytoCore, CyPromise, Artifact } from "@/types";
import {
  SingularElementArgument,
  CollectionReturnValue,
  EdgeCollection,
} from "cytoscape";

export function getArtifactSubTree(
  cyPromise: CyPromise,
  artifact: Artifact
): Promise<string[]> {
  return cyPromise.then((cyCore: CytoCore) => {
    const artifactNode = cyCore
      .elements(`node[id = "${artifact.name}"]`)
      .first();
    const subTree = getSubTree(cyCore, artifactNode);
    return subTree.map((a) => a.data().id);
  });
}

const typeHierarchy = [
  // todo: Move into more specific file
  "hazard",
  "requirement",
  "design",
  "environmentalassumption",
];

function getSubTree(
  cyCore: CytoCore,
  root: SingularElementArgument,
  artifactsSeen: string[] = []
): CollectionReturnValue {
  let subTree = cyCore.collection();
  subTree = subTree.union(root);
  artifactsSeen.push(root.data().id);
  cyCore
    .edges()
    .filter((e) => e.source() === root)
    .forEach((e) => {
      const node = e.target();
      const nodeType = node.data().artifactType;
      const rootType = root.data().artifactType;
      const nodeLevel = typeHierarchy.indexOf(nodeType);
      const rootLevel = typeHierarchy.indexOf(rootType);
      if (nodeLevel === -1 || rootLevel === -1) {
        throw Error("undefined types:" + rootType + ":" + nodeType);
      }
      if (nodeLevel >= rootLevel) {
        subTree = subTree.union(getSubTree(cyCore, node, artifactsSeen));
      }
    });

  return subTree;
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
