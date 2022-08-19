import {
  ApprovalType,
  ArtifactDeltaState,
  ColumnDataType,
  DocumentType,
  FTANodeType,
  SafetyCaseType,
  SelectOption,
} from "@/types";
import { enumToDisplay } from "@/util/string-helper";

/**
 * Converts an enum value into a selectable option with a title case name.
 *
 * @param enumValue - The enum value in upper snake case to convert.
 * @param name - The name of the option, which will bne generated if not given.
 * @return The selectable option.
 */
export function createEnumOption(
  enumValue: string,
  name?: string
): SelectOption {
  return { id: enumValue, name: name || enumToDisplay(enumValue) };
}

/**
 * Returns display names for each document type.
 *
 * @return The select option names and ids.
 */
export function documentTypeOptions(): SelectOption[] {
  return [
    createEnumOption(DocumentType.ARTIFACT_TREE, "Default"),
    createEnumOption(DocumentType.FTA, "FTA"),
    createEnumOption(DocumentType.SAFETY_CASE),
    createEnumOption(DocumentType.FMEA, "FMEA"),
    createEnumOption(DocumentType.FMECA, "FMECA"),
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
    createEnumOption(SafetyCaseType.CONTEXT),
    createEnumOption(SafetyCaseType.GOAL),
    createEnumOption(SafetyCaseType.STRATEGY),
    createEnumOption(SafetyCaseType.SOLUTION),
  ];
}

/**
 * Returns display names for each logic type.
 *
 * @return The select option names and ids.
 */
export function logicTypeOptions(): SelectOption[] {
  return [createEnumOption(FTANodeType.AND), createEnumOption(FTANodeType.OR)];
}

/**
 * Returns display names for each column type.
 *
 * @return The select option names and ids.
 */
export function columnTypeOptions(): SelectOption[] {
  return [
    createEnumOption(ColumnDataType.FREE_TEXT, "Text"),
    createEnumOption(ColumnDataType.RELATION),
    createEnumOption(ColumnDataType.SELECT),
  ];
}

/**
 * Returns display names for each column type.
 *
 * @return The select option names and ids.
 */
export function deltaTypeOptions(): SelectOption[] {
  return [
    createEnumOption(ArtifactDeltaState.NO_CHANGE),
    createEnumOption(ArtifactDeltaState.ADDED),
    createEnumOption(ArtifactDeltaState.MODIFIED),
    createEnumOption(ArtifactDeltaState.REMOVED),
  ];
}

/**
 * Returns display names for each approval type.
 *
 * @return The select option names and ids.
 */
export function approvalTypeOptions(): SelectOption[] {
  return [
    createEnumOption(ApprovalType.UNREVIEWED),
    createEnumOption(ApprovalType.APPROVED),
    createEnumOption(ApprovalType.DECLINED),
  ];
}
