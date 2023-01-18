import {
  ArtifactDeltaState,
  WarningSchema,
  CytoCoreElementData,
  CytoCoreElementDefinition,
  FTANodeType,
  PositionSchema,
  SafetyCaseType,
  TraceLinkSchema,
} from "@/types";

/**
 * Enumerates the modes of the project graph.
 */
export enum GraphMode {
  tim = "tim",
  tree = "tree",
  table = "table",
  delta = "delta",
}

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
  warnings?: WarningSchema[];
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
  childWarnings?: WarningSchema[];

  /**
   * Whether the app is running in dark mode.
   */
  dark: boolean;
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
  position?: PositionSchema;
  /**
   * The element's cytoscape classes
   */
  classes?: string[];
}

/**
 * Defines a trace link's data in cytoscape.
 */
export interface TraceData extends CytoCoreElementData, TraceLinkSchema {
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
