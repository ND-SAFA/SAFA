import { Artifact } from "@/types";
import { SingularElementArgument } from "cytoscape";

export function isRelatedToArtifacts(
  artifactsIds: string[],
  e: SingularElementArgument
): boolean {
  if (e.isEdge()) {
    return (
      artifactsIds.includes(e.data().source) &&
      artifactsIds.includes(e.data().target)
    );
  } else {
    return artifactsIds.includes(e.data().id);
  }
}

export function isInSubtree(subtree: string[], a: Artifact): boolean {
  return subtree.length === 0 || subtree.includes(a.name);
}

export function doesNotContainType(
  ignoreTypes: string[] | undefined,
  a: Artifact
): boolean {
  return ignoreTypes === undefined || !ignoreTypes.includes(a.type);
}

export interface IgnoreTypeFilterAction {
  type: "ignore";
  ignoreType: string;
  action: "add" | "remove";
}

export interface SubtreeFilterAction {
  type: "subtree";
  artifactsInSubtree: string[];
}

export type FilterAction = IgnoreTypeFilterAction | SubtreeFilterAction;
