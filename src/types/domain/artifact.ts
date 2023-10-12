import { AttributeCollectionSchema } from "@/types";

/**
 * Enumerates the types of FTA nodes.
 */
export type FTANodeType = "AND" | "OR";

/**
 * Enumerates the types of safety cases.
 */
export type SafetyCaseType = "GOAL" | "SOLUTION" | "CONTEXT" | "STRATEGY";

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
   * Whether the artifact is a code artifact.
   */
  isCode: boolean;
  /**
   * The ids of documents that display this artifact.
   */
  documentIds: string[];
  /**
   * Represents a collection of custom attributes on an artifact.
   */
  attributes?: AttributeCollectionSchema;
}

/**
 * Defines an artifact with its custom fields flattened into the artifact data.
 */
export type FlatArtifact = Record<string, string | boolean> &
  Pick<ArtifactSchema, "id" | "name" | "type" | "summary" | "isCode">;
