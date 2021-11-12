import { CytoCore } from "@/types";
import { Artifact } from "@/types";
import {
  SingularElementArgument,
  CollectionReturnValue,
  EdgeCollection,
} from "cytoscape";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export let resolveCy: any = null;

export const artifactTreeCyPromise: Promise<CytoCore> = new Promise(
  (resolve) => (resolveCy = resolve)
);

export function getArtifactSubTree(artifact: Artifact): Promise<string[]> {
  return artifactTreeCyPromise.then((cyCore: CytoCore) => {
    const artifactNode = cyCore
      .elements(`node[id = "${artifact.name}"]`)
      .first();
    const subTree = getSubTree(cyCore, artifactNode);
    return subTree.map((a) => a.data().id);
  });
}

const typeHierarchy = [
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
 * Picks a random node and follows the parents until no more exist.
 *
 * @param cyPromise - A promise returning cytoscape whose root node is returned.
 * @param currentNode - Defines where we are in the tree during recursion.
 */
export async function getRootNode(
  cyPromise: Promise<CytoCore>,
  currentNode?: SingularElementArgument
): Promise<SingularElementArgument> {
  const cyCore = await cyPromise;

  if (cyCore.nodes().length === 0) {
    throw Error("Root node does not exist because no nodes are in view.");
  }

  if (currentNode === undefined) {
    currentNode = getMostConnectedNode(cyCore);
  }

  const edgesOutOfNode: EdgeCollection = cyCore
    .edges()
    .filter((e) => e.target() === currentNode);

  if (edgesOutOfNode.length === 0) {
    return currentNode;
  } else {
    return getRootNode(cyPromise, edgesOutOfNode[0].source());
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
