/**
 * Represents a node's subtree, parents, and children.
 */
export interface SubtreeItem {
  /**
   * The parent ids of this node.
   */
  parents: string[];
  /**
   * The child ids of this node.
   */
  children: string[];
  /**
   * The subtree ids of this node.
   */
  subtree: string[];
}

/**
 * Maps each node to its related nodes.
 */
export type SubtreeMap = Record<string, SubtreeItem>;
