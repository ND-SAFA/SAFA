import {
  ArtifactDeltaState,
  WarningModel,
  CytoCoreElementData,
  CytoCoreElementDefinition,
  FTANodeType,
  LayoutPosition,
  SafetyCaseType,
  TraceLinkModel,
} from "@/types";

/**
 * Defines an artifact's data in cytoscape.
 */
export interface ArtifactData extends CytoCoreElementData {
  /**
   * The id of the artifact.
   */
  id: string;
  /**
   * The content of the artifact.
   */
  body: string;
  /**
   * Any warnings generated from the artifact.
   */
  warnings?: WarningModel[];
  /**
   * The name of the artifact.
   */
  artifactName: string;
  /**
   * The type of the artifact.
   */
  artifactType: string;
  /**
   * For FTA nodes, the logic type of the artifact.
   */
  logicType?: FTANodeType;
  /**
   * For safety case nodes, the type of the artifact.
   */
  safetyCaseType?: SafetyCaseType;
  /**
   * The state of changes to the artifact.
   */
  artifactDeltaState: ArtifactDeltaState;
  /**
   * Whether the artifact is selected.
   */
  isSelected: boolean;
  /**
   * The opacity of this artifact.
   */
  opacity: number;

  /**
   * The number of hidden child elements.
   */
  hiddenChildren?: number;
  /**
   * The delta states of any hidden children.
   */
  childDeltaStates?: ArtifactDeltaState[];
  /**
   * Any warnings in child elements.
   */
  childWarnings?: WarningModel[];
}

/**
 * Defines an artifact element.
 */
export interface ArtifactCytoCoreElement extends CytoCoreElementDefinition {
  /**
   * The element's stored data.
   */
  data: ArtifactData;
  /**
   * The artifact's position in the graph
   */
  position?: LayoutPosition;
  /**
   * The element's cytoscape classes
   */
  classes?: string[];
}

/**
 * Defines a trace link's data in cytoscape.
 */
export interface TraceData extends CytoCoreElementData, TraceLinkModel {
  /**
   * The cytoscape element id to point from.
   */
  source: string;
  /**
   * The cytoscape element id to point toward.
   */
  target: string;
  /**
   * The count to display on the trace link.
   */
  count: number;
  /**
   * The state of changes to the trace link.
   */
  deltaType: ArtifactDeltaState;
  /**
   * Whether to fade this trace link.
   */
  faded?: boolean;
}

/**
 * Defines a trace link element.
 */
export interface TraceCytoCoreElement extends CytoCoreElementDefinition {
  /**
   * The element's stored data.
   */
  data: TraceData;
  /**
   * The element's cytoscape classes
   */
  classes?: string[];
}
