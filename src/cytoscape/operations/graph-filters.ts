import { Artifact } from "@/types";
import { SingularElementArgument } from "cytoscape";

export function isRelatedToArtifacts(
  artifactsIds: string[],
  e: SingularElementArgument
): boolean {
  if (e.isEdge()) {
    return (
      artifactsIds.includes(e.data().sourceId) &&
      artifactsIds.includes(e.data().targetId)
    );
  } else {
    return artifactsIds.includes(e.data().id);
  }
}

export function isInSubtree(subtreeIds: string[], artifact: Artifact): boolean {
  return subtreeIds.length === 0 || subtreeIds.includes(artifact.id);
}

export function doesNotContainType(
  ignoreTypes: string[] | undefined,
  a: Artifact
): boolean {
  return ignoreTypes === undefined || !ignoreTypes.includes(a.type);
}
