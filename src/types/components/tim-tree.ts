import { CytoCoreElementData, CytoCoreElementDefinition } from "@/types";

export interface TypeNodeDefinitions extends CytoCoreElementDefinition {
  data: ArtifactTypeNodeData;
}
export interface ArtifactTypeNodeData extends CytoCoreElementData {
  count: number;
}
