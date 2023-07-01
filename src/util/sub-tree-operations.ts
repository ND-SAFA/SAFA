import { ArtifactSchema } from "@/types";

/**
 * Returns a list of all child artifact ids of the given parents that match the given types.
 *
 * @param parentIds - The parent artifacts to get the subtrees of.
 * @param includedChildTypes - The child artifact types to find.
 * @param getSubtree - Returns the subtree node ids of an artifact.
 * @param getArtifact - Returns a matching artifact by id.
 *
 * @return The ids of all child artifacts that match.
 */
export function getMatchingChildren(
  parentIds: string[],
  includedChildTypes: string[],
  getSubtree: (id: string) => string[],
  getArtifact: (id: string) => ArtifactSchema | undefined
): string[] {
  if (includedChildTypes.length === 0) return [];

  const childArtifactIds = new Set<string>();

  parentIds.forEach((parentId) => {
    getSubtree(parentId).forEach((childId) => {
      const artifact = getArtifact(childId);

      if (!artifact || !includedChildTypes.includes(artifact.type)) return;

      childArtifactIds.add(childId);
    });
  });

  return Array.from(childArtifactIds);
}
