import { CytoCoreElementData, CytoCoreElementDefinition } from "@/types";

/**
 * Defines a tim node in cytoscape.
 */
export interface TimNodeDefinition extends CytoCoreElementDefinition {
  data: TimNodeData;
}
/**
 * Defines a tim node's data in cytoscape.
 */
export interface TimNodeData extends CytoCoreElementData {
  count: number;
}
