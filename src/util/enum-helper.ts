import {
  ColumnDataType,
  DocumentType,
  FTANodeType,
  SafetyCaseType,
  SelectOption,
} from "@/types";

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
    { id: DocumentType.FMECA, name: "FMECA" },
  ];
}

/**
 * Returns the document types of artifacts that can be created on a given document.
 *
 * @return The select option names and ids.
 */
export function documentTypeMap(): { [type in DocumentType]: SelectOption[] } {
  const options = documentTypeOptions();

  return {
    [DocumentType.ARTIFACT_TREE]: [options[0]],
    [DocumentType.FTA]: [options[0], options[1]],
    [DocumentType.SAFETY_CASE]: [options[0], options[2]],
    [DocumentType.FMEA]: [options[0], options[3]],
    [DocumentType.FMECA]: [options[0], options[4]],
  };
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

/**
 * Returns display names for each logic type.
 *
 * @return The select option names and ids.
 */
export function logicTypeOptions(): SelectOption[] {
  return [
    { id: FTANodeType.AND, name: "And" },
    { id: FTANodeType.OR, name: "Or" },
  ];
}

/**
 * Returns display names for each column type.
 *
 * @return The select option names and ids.
 */
export function columnTypeOptions(): SelectOption[] {
  return [
    { id: ColumnDataType.FREE_TEXT, name: "Text" },
    { id: ColumnDataType.RELATION, name: "Relation" },
    { id: ColumnDataType.SELECT, name: "Select" },
  ];
}
