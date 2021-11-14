import { CytoCoreElementData, CytoCoreElementDefinition } from "@/types";

export interface TimNodeDefinition extends CytoCoreElementDefinition {
  data: TimNodeData;
}
export interface TimNodeData extends CytoCoreElementData {
  count: number;
}
