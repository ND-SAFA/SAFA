"use strict";
exports.__esModule = true;
exports.doesNotContainType = exports.isInSubtree = exports.isRelatedToArtifacts = void 0;
/**
 * Returns whether the element is either:
 * 1. A node included in the given artifact ids.
 * 2. A link between two of the given artifact ids.
 *
 * @param artifactsIds - The artifacts to check within.
 * @param element - The element to check.
 * @return Whether the element is related.
 */
function isRelatedToArtifacts(artifactsIds, element) {
    if (element.isEdge()) {
        return (artifactsIds.includes(element.data().sourceId) &&
            artifactsIds.includes(element.data().targetId));
    }
    else {
        return artifactsIds.includes(element.data().id);
    }
}
exports.isRelatedToArtifacts = isRelatedToArtifacts;
/**
 * Returns whether the artifact is in the given subtree, or the subtree is empty.
 *
 * @param subtreeIds - The artifacts to check within.
 * @param artifact - The artifact to find.
 * @return Whether the element in the subtree or the subtree is empty.
 */
function isInSubtree(subtreeIds, artifact) {
    return subtreeIds.length === 0 || subtreeIds.includes(artifact.id);
}
exports.isInSubtree = isInSubtree;
/**
 * Returns the artifact is ignored.
 *
 * @param ignoreTypes - The ignored types.
 * @param artifact - The artifact to check.
 * @return Whether the artifact is not ignored.
 */
function doesNotContainType(ignoreTypes, artifact) {
    return ignoreTypes === undefined || !ignoreTypes.includes(artifact.type);
}
exports.doesNotContainType = doesNotContainType;
