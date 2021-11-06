import { CytoCore } from "@/types";
import { Artifact } from "@/types";
import { SingularElementArgument, CollectionReturnValue } from "cytoscape";

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
