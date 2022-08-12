import { IdentifierModel } from "@/types/domain/project";
import { ArtifactPositions } from "@/types";

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
 * Enumerates the types of columns in a table document.
 */
export enum ColumnDataType {
  FREE_TEXT = "FREE_TEXT",
  RELATION = "RELATION",
  SELECT = "SELECT",
}

/**
 * Represents a column definition in a table-like document.
 */
export interface ColumnModel {
  /**
   * The ID of this column.
   */
  id: string;
  /**
   * The name of this column.
   */
  name: string;
  /**
   * The type of data this column represents.
   */
  dataType: ColumnDataType;
  /**
   * Whether this column must have a non-empty value.
   */
  required: boolean;
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
  layout: ArtifactPositions;
  /**
   * Defines the columns of a table-like document.
   */
  columns?: ColumnModel[];
}
