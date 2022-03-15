import { DocumentType, SafetyCaseType, SelectOption } from "@/types";

/**
 * Returns display names for each document type.
 *
 * @return The select option names and ids.
 */
export function documentTypeOptions(): SelectOption[] {
  return [
    { id: DocumentType.ARTIFACT_TREE, name: "Default" },
    { id: DocumentType.FTA, name: "FTA" },
    { id: DocumentType.SAFETY_CASE, name: "Safety Case" },
    { id: DocumentType.FMEA, name: "FMEA" },
  ];
}

/**
 * Returns whether the given document represents a table.
 *
 * @param type - The current document type.
 * @return Whether the type is for a table.
 */
export function isTableDocument(type: DocumentType): boolean {
  const tableDocuments = [DocumentType.FMEA, DocumentType.FMECA];

  return tableDocuments.includes(type);
}

/**
 * Returns display names for each safety case type.
 *
 * @return The select option names and ids.
 */
export function safetyCaseOptions(): SelectOption[] {
  return [
    { id: SafetyCaseType.CONTEXT, name: "Context" },
    { id: SafetyCaseType.GOAL, name: "Goal" },
    { id: SafetyCaseType.STRATEGY, name: "Strategy" },
    { id: SafetyCaseType.SOLUTION, name: "Solution" },
  ];
}
