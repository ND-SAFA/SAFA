import { LayoutPositionsModel } from "@/types";
import { IdentifierModel } from "@/types/domain/project";

/**
 * Enumerates the type of documents supported by SAFA.
 */
export enum DocumentType {
  ARTIFACT_TREE = "ARTIFACT_TREE",
  FTA = "FTA",
  SAFETY_CASE = "SAFETY_CASE",
  FMEA = "FMEA",
  FMECA = "FMECA",
}

/**
 * Defines a specific document.
 */
export interface DocumentModel {
  /**
   * The id of this document.
   */
  documentId: string;
  /**
   * The project associated with this document.
   */
  project: IdentifierModel;
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
  /**
   * Map of document ids to their artifact positions.
   */
  layout: LayoutPositionsModel;
}
