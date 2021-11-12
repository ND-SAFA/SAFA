import { ArtifactDeltaState } from "./delta";
import { CytoCoreElementData } from "@/types/cytoscape";

/**
 * Defines an artifact file.
 */
export interface Artifact {
  /**
   * The name of the artifact.
   */
  name: string;
  /**
   * A summary of the artifact.
   */
  summary?: string;
  /**
   * The content of the artifact.
   */
  body: string;
  /**
   * The type of the artifact.
   */
  type: string;
}

/**
 * Defines an artifact's data.
 */
export interface ArtifactData extends CytoCoreElementData {
  /**
   * The content of the artifact.
   */
  body: string;
  /**
   * Any warnings generated from the artifact.
   */
  warnings?: ArtifactWarning[];
  /**
   * The name of the artifact.
   */
  artifactName: string;
  /**
   * The type of the artifact.
   */
  artifactType: string;
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
}

/**
 * Defines an artifact warning.
 */
export interface ArtifactWarning {
  /**
   * The artifact rule name.
   */
  ruleName: string;
  /**
   * The artifact rule message.
   */
  ruleMessage: string;
}

/**
 * A collection of warnings for all artifacts.
 */
export type ProjectWarnings = Record<string, ArtifactWarning[]>;

/**
 * Returns an artifact matching the given query, if one exists.
 */
export type ArtifactQueryFunction = (q: string) => Artifact | undefined;
