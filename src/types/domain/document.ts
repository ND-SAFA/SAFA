/**
 * Enumerates the type of documents supported by SAFA
 */
import { ProjectIdentifier } from "@/types";

export enum DocumentType {
  ARTIFACT_TREE = "ARTIFACT_TREE",
  FTA = "FTA",
  SAFETY_CASE = "SAFETY_CASE",
}

/**
 * Defines a specific document.
 */
export interface ProjectDocument {
  /**
   * The id of this document.
   */
  documentId: string;
  /**
   * The project associated with this document.
   */
  project: ProjectIdentifier;
  /**
   * The name of the document.
   */
  name: string;
  /**
   * The description of the document.
   */
  description: string;
  /**
   * The type of document.
   */
  type: DocumentType;
  /**
   * The ids of artifacts displayed within this document.
   */
  artifactIds: string[];
}
