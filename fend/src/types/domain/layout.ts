/**
 * The position of a node within a graph.
 * A node’s position refers to the centre point of its body.
 */
export interface PositionSchema {
  /**
   * # of pixes right from the top-left  corner.
   */
  x: number;
  /**
   * # of pixels down from the top-left corner.
   */
  y: number;
}

/**
 * Maps artifact ids to their coordinates on the graph.
 */
export type LayoutPositionsSchema = Record<string, PositionSchema>;
