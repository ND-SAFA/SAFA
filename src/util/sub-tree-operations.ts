import {
  ArtifactModel,
  ArtifactQueryFunction,
  InternalTraceType,
  SubtreeItem,
  SubtreeLinkModel,
  SubtreeMap,
  TraceLinkModel,
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
  getArtifact: ArtifactQueryFunction
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
  traces: TraceLinkModel[],
  phantomLinkIds: string[],
  nodesInSubtree: string[],
  rootId: string,
  childId: string
): (isIncoming: boolean) => SubtreeLinkModel[] {
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
        const base: SubtreeLinkModel = {
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
  artifacts: ArtifactModel[],
  traces: TraceLinkModel[]
): SubtreeMap {
  const computedSubtrees = {};

  return artifacts
    .map((artifact) => ({
      [artifact.id]: getSubtree(
        artifacts,
        traces,
        artifact.id,
        computedSubtrees
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
 * @return The child ids in the subtree.
 */
function getSubtree(
  artifacts: ArtifactModel[],
  traces: TraceLinkModel[],
  artifactId: string,
  subtreeMapCache: SubtreeMap
): SubtreeItem {
  const currentItem: SubtreeItem = {
    parents: [],
    children: [],
    subtree: [],
  };

  if (artifactId in subtreeMapCache) {
    return subtreeMapCache[artifactId];
  }

  for (const childId of getChildren(artifacts, traces, artifactId)) {
    if (!(childId in subtreeMapCache)) {
      subtreeMapCache[childId] = getSubtree(
        artifacts,
        traces,
        childId,
        subtreeMapCache
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
  artifacts: ArtifactModel[],
  traces: TraceLinkModel[],
  artifactId: string
): string[] {
  return traces
    .filter(({ targetId }) => targetId === artifactId)
    .map(({ sourceId }) => sourceId);
}

/**
 * Returns the top most parent from all elements in the cytoscape object.
 * Starting at the node with most edges, its parent is followed until no
 * more exist. If a loop is encountered, then the first repeated node is returned.
 *
 * @param artifacts - All artifacts in the system.
 * @param traces - All traces in the system.
 * @param currentArtifactId - Defines where we are in the tree during recursion.
 * @param traversedNodes - A list of all traversed node IDs to avoid loops.
 * @return The root node.
 */
export async function getRootNode(
  artifacts: ArtifactModel[],
  traces: TraceLinkModel[],
  currentArtifactId?: string,
  traversedNodes: string[] = []
): Promise<string | undefined> {
  if (traces.length === 0) return;

  if (currentArtifactId === undefined) {
    currentArtifactId = getMostConnectedNode(artifacts, traces);
  }

  // Avoid getting stuck in cycles.
  if (traversedNodes.includes(currentArtifactId)) {
    return currentArtifactId;
  } else {
    traversedNodes.push(currentArtifactId);
  }

  const edgesOutOfNode = traces.filter(
    ({ targetId }) => targetId === currentArtifactId
  );

  if (edgesOutOfNode.length === 0) {
    return currentArtifactId;
  } else {
    return getRootNode(
      artifacts,
      traces,
      edgesOutOfNode[0].sourceId,
      traversedNodes
    );
  }
}

/**
 * Returns the node in given Cytoscape instance with the most connected edges.
 *
 * @param artifacts - All artifacts in the system.
 * @param traces - All traces in the system.
 * @return The found node.
 */
function getMostConnectedNode(
  artifacts: ArtifactModel[],
  traces: TraceLinkModel[]
): string {
  let max = -1;
  let maxId = "";
  const counts: Record<string, number> = {};

  const increaseCounts = (name: string) => {
    if (name in counts) {
      counts[name]++;
    } else {
      counts[name] = 1;
    }
  };

  traces.forEach(({ sourceId, targetId }) => {
    increaseCounts(sourceId);
    increaseCounts(targetId);
  });

  for (const [id, count] of Object.entries(counts)) {
    if (count > max) {
      max = count;
      maxId = id;
    }
  }

  return maxId;
}
