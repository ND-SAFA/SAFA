import {
  ApprovalType,
  ArtifactDeltaState,
  AttributeType,
  CreatorTabTypes,
  DocumentType,
  FTANodeType,
  ModelShareType,
  ModelTabTypes,
  ModelType,
  ProjectRole,
  SafetyCaseType,
  SelectOption,
  SettingsTabTypes,
  TracePredictionTabTypes,
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
 * Returns display names for each delta type.
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

/**
 * Returns display names for each trace model type.
 *
 * @return The select option names and ids.
 */
export function traceModelOptions(): SelectOption[] {
  return [
    createEnumOption(
      ModelType.NLBert,
      "Slower, higher quality links. Traces free-text artifacts to other free-text artifacts."
    ),
    createEnumOption(
      ModelType.PLBert,
      "Slower, higher quality links. Traces free-text artifacts to source code."
    ),
    createEnumOption(
      ModelType.AutomotiveBert,
      "Slower, high quality links for automotive projects."
    ),
    createEnumOption(ModelType.VSM, "Faster, lower quality links."),
  ];
}

/**
 * Returns display names for project role type.
 *
 * @return The select option names and ids.
 */
export function projectRoleOptions(): SelectOption[] {
  return [
    createEnumOption(ProjectRole.OWNER),
    createEnumOption(ProjectRole.ADMIN),
    createEnumOption(ProjectRole.EDITOR),
    createEnumOption(ProjectRole.VIEWER),
  ];
}

/**
 * Returns display names for model share options.
 *
 * @return The select option names and ids.
 */
export function modelShareOptions(): SelectOption[] {
  return [
    createEnumOption(ModelShareType.CLONE, "Clone the model"),
    createEnumOption(ModelShareType.REUSE, "Reuse the same model"),
  ];
}

/**
 * Returns display names for project creator tabs.
 *
 * @return The select option names and ids.
 */
export function creatorTabOptions(): SelectOption[] {
  return [
    createEnumOption(CreatorTabTypes.standard, "Standard Upload"),
    createEnumOption(CreatorTabTypes.bulk, "Bulk Upload"),
    createEnumOption(CreatorTabTypes.import, "Integrations Import"),
  ];
}

/**
 * Returns display names for model editor tabs.
 *
 * @return The select option names and ids.
 */
export function modelEditorTabOptions(): SelectOption[] {
  return [
    createEnumOption(ModelTabTypes.training, "Training"),
    createEnumOption(ModelTabTypes.evaluation, "Evaluation"),
  ];
}

/**
 * Returns display names for trace prediction tabs.
 *
 * @return The select option names and ids.
 */
export function tracePredictionTabOptions(): SelectOption[] {
  return [
    createEnumOption(TracePredictionTabTypes.models, "Models"),
    createEnumOption(TracePredictionTabTypes.generation, "Trace Generation"),
    createEnumOption(TracePredictionTabTypes.approval, "Trace Approval"),
  ];
}

/**
 * Returns display names for project settings tabs.
 *
 * @return The select option names and ids.
 */
export function settingsTabOptions(): SelectOption[] {
  return [
    createEnumOption(SettingsTabTypes.members, "Members"),
    createEnumOption(SettingsTabTypes.upload, "Data Upload"),
    createEnumOption(SettingsTabTypes.integrations, "Data Integrations"),
    createEnumOption(SettingsTabTypes.artifacts, "Artifact Types"),
    createEnumOption(SettingsTabTypes.attributes, "Custom Attributes"),
  ];
}

/**
 * Returns display names for model training tabs.
 *
 * @return The select option names and ids.
 */
export function trainingTabOptions(): SelectOption[] {
  return [
    createEnumOption("documents", "Documents"),
    createEnumOption("repositories", "Repositories"),
    createEnumOption("keywords", "Keywords"),
    createEnumOption("project", "Project Data"),
  ];
}

/**
 * Returns display names for table view tabs.
 *
 * @return The select option names and ids.
 */
export function tableViewTabOptions(): SelectOption[] {
  return [
    createEnumOption("artifacts", "Artifacts"),
    createEnumOption("traceLinks", "Trace Links"),
  ];
}

/**
 * Returns display names for attribute types.
 *
 * @return The select option names and ids.
 */
export function attributeTypeOptions(): SelectOption[] {
  return [
    createEnumOption(AttributeType.text, "Text"),
    createEnumOption(AttributeType.paragraph, "Paragraph"),
    createEnumOption(AttributeType.select, "Select"),
    createEnumOption(AttributeType.multiselect, "Multiselect"),
    createEnumOption(AttributeType.relation, "Relation"),
    createEnumOption(AttributeType.date, "Date"),
    createEnumOption(AttributeType.int, "Integer"),
    createEnumOption(AttributeType.float, "Number"),
    createEnumOption(AttributeType.boolean, "Yes/No"),
  ];
}
