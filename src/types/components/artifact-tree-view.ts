import { ArtifactData, CytoCoreElementDefinition } from "@/types";

/**
 * Defines an artifact element.
 */
export interface ArtifactCytoCoreElement extends CytoCoreElementDefinition {
  data: ArtifactData;
}
