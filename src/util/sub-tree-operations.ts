import {
  ArtifactSchema,
  InternalTraceType,
  SubtreeItem,
  SubtreeLinkSchema,
  SubtreeMap,
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
 * TODO: this is very inefficient.
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

/**
 * Computes the subtree map of given artifacts.
 *
 * @param artifacts - All artifacts in the system.
 * @param traces - All traces in the system.
 * @return The computed subtree map.
 */
export function createSubtreeMap(
  artifacts: ArtifactSchema[],
  traces: TraceLinkSchema[]
): SubtreeMap {
  const computedSubtrees = {};
  const traversedIds: string[] = [];

  return artifacts
    .map((artifact) => ({
      [artifact.id]: getSubtree(
        artifacts,
        traces,
        artifact.id,
        computedSubtrees,
        traversedIds
      ),
    }))
    .reduce((acc, cur) => ({ ...acc, ...cur }), {});
}

/**
 * Returns list of children names for artifact specified.
 *
 * @param artifacts - All artifacts in the system.
 * @param traces - All traces in the system.
 * @param artifactId - The id of the root artifact whose subtree is being calculated.
 * @param subtreeMapCache - A cache of previously calculated subtrees.
 * @param traversedIds - A cache of previously traversed artifacts.
 * @return The child ids in the subtree.
 */
function getSubtree(
  artifacts: ArtifactSchema[],
  traces: TraceLinkSchema[],
  artifactId: string,
  subtreeMapCache: SubtreeMap,
  traversedIds: string[]
): SubtreeItem {
  const currentItem: SubtreeItem = {
    parents: [],
    children: [],
    subtree: [],
  };

  if (artifactId in subtreeMapCache || traversedIds.includes(artifactId)) {
    return subtreeMapCache[artifactId] || currentItem;
  }

  traversedIds.push(artifactId);

  for (const childId of getChildren(artifacts, traces, artifactId)) {
    if (!(childId in subtreeMapCache)) {
      subtreeMapCache[childId] = getSubtree(
        artifacts,
        traces,
        childId,
        subtreeMapCache,
        traversedIds
      );
    }

    subtreeMapCache[childId].parents.push(artifactId);
    currentItem.children.push(childId);
    currentItem.subtree = [
      ...currentItem.subtree,
      ...[...subtreeMapCache[childId].subtree, childId].filter(
        (id) => !currentItem.subtree.includes(id)
      ),
    ];
  }

  subtreeMapCache[artifactId] = currentItem;

  return currentItem;
}

/**
 * Returns list of artifact ids corresponding to children of artifact.
 *
 * @param artifacts - All artifacts in the system.
 * @param traces - All traces in the system.
 * @param artifactId - The id of the root artifact whose subtree is being calculated.
 * @return The computed child artifact ids.
 */
function getChildren(
  artifacts: ArtifactSchema[],
  traces: TraceLinkSchema[],
  artifactId: string
): string[] {
  return traces
    .filter(({ targetId }) => targetId === artifactId)
    .map(({ sourceId }) => sourceId);
}
