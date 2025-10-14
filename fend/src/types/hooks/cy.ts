import { NodeSingular } from "cytoscape";

/**
 * Represents configuration for building a cytoscape graph,
 * primarily to inject dependencies on other stores.
 */
export interface CyConfiguration {
  /**
   * Returns whether the given source and target nodes can be connected.
   * @param source - The source node.
   * @param target - The target node.
   * @return Whether they can be connected.
   */
  canCreateTrace(source: NodeSingular, target: NodeSingular): boolean;
  /**
   * Called when a new trace link is created.
   * @param source - The source node.
   * @param target - The target node.
   */
  handleCreateTrace(source: NodeSingular, target: NodeSingular): void;
}
