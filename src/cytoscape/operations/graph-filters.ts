import { SingularElementArgument } from "cytoscape";
import { ArtifactModel } from "@/types";

/**
 * Returns whether the element is either:
 * 1. A node included in the given artifact ids.
 * 2. A link between two of the given artifact ids.
 *
 * @param artifactsIds - The artifacts to check within.
 * @param element - The element to check.
 * @return Whether the element is related.
 */
export function isRelatedToArtifacts(
  artifactsIds: string[],
  element: SingularElementArgument
): boolean {
  if (element.isEdge()) {
    return (
      artifactsIds.includes(element.data().sourceId) &&
      artifactsIds.includes(element.data().targetId)
    );
  } else {
    return artifactsIds.includes(element.data().id);
  }
}

/**
 * Returns whether the artifact is in the given subtree, or the subtree is empty.
 *
 * @param subtreeIds - The artifacts to check within.
 * @param artifact - The artifact to find.
 * @return Whether the element in the subtree or the subtree is empty.
 */
export function isInSubtree(
  subtreeIds: string[],
  artifact: ArtifactModel
): boolean {
  return subtreeIds.length === 0 || subtreeIds.includes(artifact.id);
}

/**
 * Returns the artifact is ignored.
 *
 * @param ignoreTypes - The ignored types.
 * @param artifact - The artifact to check.
 * @return Whether the artifact is not ignored.
 */
export function doesNotContainType(
  ignoreTypes: string[] | undefined,
  artifact: ArtifactModel
): boolean {
  return ignoreTypes === undefined || !ignoreTypes.includes(artifact.type);
}
