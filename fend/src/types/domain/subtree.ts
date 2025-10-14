/**
 * Represents a node's subtree, parents, and children.
 */
export interface SubtreeItemSchema {
  /**
   * The ids of parents of this node.
   */
  parents: string[];
  /**
   The ids of children of this node.
   */
  children: string[];
  /**
   The ids of children of this node and their children, recursively.
   */
  subtree: string[];
  /**
   The ids of parents of this node and their parents, recursively.
   */
  supertree: string[];
  /**
   The ids of both the subtree and supertree combined.
   */
  neighbors: string[];
}

/**
 * Maps each node to its related nodes.
 */
export type SubtreeMapSchema = Record<string, SubtreeItemSchema>;
