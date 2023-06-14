import {
  ArtifactSchema,
  InternalTraceType,
  SubtreeLinkSchema,
  TraceLinkSchema,
} from "@/types";

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

/**
 * Creates fantom links from the given traces for all hidden subtrees.
 *
 * @param traces - The current trace links.
 * @param phantomLinkIds - The current ids of phantom links.
 * @param nodesInSubtree - The nodes in the specific subtree being hidden.
 * @param rootId - The root node id.
 * @param childId - The child node id.
 * @return Created phantom links.
 */
export function createPhantomLinks(
  traces: TraceLinkSchema[],
  phantomLinkIds: string[],
  nodesInSubtree: string[],
  rootId: string,
  childId: string
): (isIncoming: boolean) => SubtreeLinkSchema[] {
  return (isIncoming) =>
    traces
      .filter((link) => {
        const value = isIncoming ? link.targetId : link.sourceId;
        const oppoValue = isIncoming ? link.sourceId : link.targetId;
        const doesNotExist = !phantomLinkIds.includes(
          `${link.traceLinkId}-phantom`
        );
        return (
          doesNotExist &&
          value === childId &&
          !nodesInSubtree.includes(oppoValue)
        );
      })
      .map((link) => {
        const base: SubtreeLinkSchema = {
          ...link,
          traceLinkId: `${link.traceLinkId}-phantom`,
          type: InternalTraceType.SUBTREE,
          rootNode: rootId,
        };

        return isIncoming
          ? { ...base, target: rootId }
          : { ...base, source: rootId };
      });
}
