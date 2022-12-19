import { ArtifactSchema } from "@/types";

/**
 * Returns whether the artifact is in the given subtree, or the subtree is empty.
 *
 * @param subtreeIds - The artifacts to check within.
 * @param artifact - The artifact to find.
 * @return Whether the element in the subtree or the subtree is empty.
 */
export function isInSubtree(
  subtreeIds: string[],
  artifact: ArtifactSchema
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
  artifact: ArtifactSchema
): boolean {
  return ignoreTypes === undefined || !ignoreTypes.includes(artifact.type);
}
