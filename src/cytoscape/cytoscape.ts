import { CytoCore } from "@/types";
import { Artifact } from "@/types";
import {
  SingularElementArgument,
  CollectionReturnValue,
  EdgeCollection,
} from "cytoscape";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export let resolveCy: any = null;

export const cyPromise: Promise<CytoCore> = new Promise(
  (resolve) => (resolveCy = resolve)
);

export function getArtifactSubTree(artifact: Artifact): Promise<string[]> {
  return cyPromise.then((cyCore: CytoCore) => {
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
        throw Error("undefine types:" + rootType + ":" + nodeType);
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
 * @param currentNode - Defines where we are in the tree during recursion.
 */
export async function getRootNode(
  currentNode?: SingularElementArgument
): Promise<SingularElementArgument> {
  const cyCore = await cyPromise;

  if (currentNode === undefined) {
    currentNode = cyCore.nodes().first();
  }

  const edgesOutOfNode: EdgeCollection = cyCore
    .edges()
    .filter((e) => e.target() === currentNode);

  if (edgesOutOfNode.length === 0) {
    return currentNode;
  } else {
    return getRootNode(edgesOutOfNode[0].source());
  }
}
