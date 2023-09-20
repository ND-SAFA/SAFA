import { DocumentType, SelectOption } from "@/types";
import { documentTypeOptions } from "@/util/enum-helper";

/**
 * Returns the document types of artifacts that can be created on a given document.
 *
 * @return The select option names and ids.
 */
export function documentTypeMap(): Record<
  DocumentType,
  SelectOption<DocumentType>[]
> {
  const options = documentTypeOptions();

  return {
    ARTIFACT_TREE: [options[0]],
    FTA: [options[0], options[1]],
    SAFETY_CASE: [options[0], options[2]],
    FMEA: [options[0], options[3]],
    FMECA: [options[0], options[4]],
  };
}

/**
 * Returns whether the given document represents a table.
 *
 * @param type - The current document type.
 * @return Whether the type is for a table.
 */
export function isTableDocument(type: DocumentType): boolean {
  const tableDocuments: DocumentType[] = ["FMEA", "FMECA"];

  return tableDocuments.includes(type);
}
