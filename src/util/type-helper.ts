import { ArtifactTypeSchema, ProjectSchema } from "@/types";

/**
 * Represents a leaf or node within a tree of artifact types.
 */
type ArtifactTypeTree =
  | string
  | {
      type: string;
      next: ArtifactTypeTree[];
    };

/**
 * Sorts artifact types, based on their distance from each root of the type tree.
 *
 * @example A -> B, A -> C, C -> D ==> [A, B, C, D]
 *
 * @param project - The project to get the artifact types from.
 * @return The ordered artifact types, or the unordered types if an inconsistency is found.
 */
export function sortArtifactTypes(
  project: ProjectSchema
): ArtifactTypeSchema[] {
  // Find all types, not including loops, that have no parent types.
  const roots: ArtifactTypeTree[] = project.artifactTypes
    .filter(
      ({ name }) =>
        !project.traceMatrices.some(
          ({ sourceType, targetType }) =>
            name === sourceType && name !== targetType
        )
    )
    .map(({ name }) => ({ type: name, next: [] }));

  // Traverse the type tree to find the child types for each type, recursively.
  roots.forEach((root) => traverseTypeTree(root, project));

  // Order the types based on their level in the type tree.
  const orderedTypes = getOrderFromRoots(roots, project);

  // Validate that all types are included in the ordered types, otherwise return the unordered types.
  return orderedTypes.length === project.artifactTypes.length
    ? orderedTypes
    : project.artifactTypes;
}

function traverseTypeTree(
  root: ArtifactTypeTree,
  project: ProjectSchema,
  visitedNodes: string[] = []
): ArtifactTypeTree {
  if (typeof root !== "string") {
    project.traceMatrices.forEach(({ sourceType, targetType }) => {
      if (
        targetType === root.type &&
        sourceType !== targetType &&
        !visitedNodes.includes(sourceType)
      ) {
        root.next.push(
          traverseTypeTree({ type: sourceType, next: [] }, project, [
            ...visitedNodes,
            root.type,
          ])
        );
      }
    });
  }

  return root;
}

/**
 * Returns the artifact types in order based on their level in the type tree.
 * Recursively traverses each layer of the type tree, starting with the root layer,
 * to order the artifact types.
 *
 * @example A -> B, A -> C, C -> D ==> [A, B, C, D]
 *
 * @param roots - The roots of the type tree.
 * @param project - The project to get the artifact types from.
 * @return The ordered artifact types.
 */
function getOrderFromRoots(
  roots: ArtifactTypeTree[],
  project: ProjectSchema
): ArtifactTypeSchema[] {
  const orderedTypes: ArtifactTypeSchema[] = [];
  let currentLevel = roots;

  while (currentLevel.length > 0) {
    const nextLevel: ArtifactTypeTree[] = [];

    currentLevel.forEach((node) => {
      if (
        typeof node !== "string" &&
        !orderedTypes.find(({ name }) => name === node.type)
      ) {
        orderedTypes.push(
          project.artifactTypes.find(({ name }) => name === node.type)!
        );
        nextLevel.push(...node.next);
      } else if (
        typeof node === "string" &&
        !orderedTypes.find(({ name }) => name === node)
      ) {
        orderedTypes.push(
          project.artifactTypes.find(({ name }) => name === node)!
        );
      }
    });

    currentLevel = nextLevel;
  }

  return orderedTypes;
}
