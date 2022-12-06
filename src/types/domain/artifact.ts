import { AttributeCollectionSchema } from "./attribute";
import { DocumentType } from "./document";

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
 * A map from each safety case types to what they can trace to.
 */
export const allowedSafetyCaseTypes: Record<SafetyCaseType, SafetyCaseType[]> =
  {
    [SafetyCaseType.GOAL]: [SafetyCaseType.GOAL, SafetyCaseType.STRATEGY],
    [SafetyCaseType.SOLUTION]: [SafetyCaseType.GOAL],
    [SafetyCaseType.CONTEXT]: [SafetyCaseType.GOAL],
    [SafetyCaseType.STRATEGY]: [SafetyCaseType.GOAL],
  };

/**
 * Defines an artifact of a project.
 */
export interface ArtifactSchema {
  /**
   * A unique UUID identifying an artifact across versions.
   */
  id: string;
  /**
   * A unique UUID identifying an artifact across versions.
   */
  baseEntityId?: string;
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
  attributes?: AttributeCollectionSchema;
}

/**
 * Defines an artifact with its custom fields flattened into the artifact data.
 */
export type FlatArtifact = ArtifactSchema & Record<string, string>;
