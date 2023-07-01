import { DocumentType, SelectOption } from "@/types";
import { documentTypeOptions } from "@/util/enum-helper";

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
