/**
 * Defines an ignore filter action.
 */
export interface IgnoreTypeFilterAction {
  type: "ignore";
  ignoreType: string;
  action: "add" | "remove";
}

/**
 * Defines an subtree filter action.
 */
export interface SubtreeFilterAction {
  type: "subtree";
  nodeIds: string[];
  centerIds?: string[];
}

/**
 * Defines a general filter action.
 */
export type FilterAction = IgnoreTypeFilterAction | SubtreeFilterAction;
