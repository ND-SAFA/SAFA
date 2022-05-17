import { DocumentType } from "@/types/domain/document";

/**
 * Enumerates the types of FTA nodes.
 */
export enum FTANodeType {
  OR = "OR",
  AND = "AND",
}

/**
 * Enumerates the types of safety cases.
 */
export enum SafetyCaseType {
  GOAL = "GOAL",
  SOLUTION = "SOLUTION",
  CONTEXT = "CONTEXT",
  STRATEGY = "STRATEGY",
}

/**
 * Defines an artifact file.
 */
export interface Artifact {
  /**
   * A unique UUID identifying an artifact across versions.
   */
  id: string;
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
  /**
   * The ids of documents that display this artifact.
   */
  documentIds: string[];
  /**
   * The type of document this artifact is displayed in.
   */
  documentType?: DocumentType;
  /**
   * For FTA logic nodes,  the logical operator of this node.
   */
  logicType?: FTANodeType;
  /**
   * For safety case nodes, the type of safety case node.
   */
  safetyCaseType?: SafetyCaseType;
  /**
   * Represents a collection of custom attributes on an artifact.
   */
  customFields?: Record<string, string>;
}

/**
 * Defines an artifact with its custom fields flattened into the artifact data.
 */
export type FlatArtifact = Artifact & Record<string, string>;

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
export type ArtifactQueryFunction = (q: string) => Artifact;
