import {
  ApprovalType,
  ArtifactDeltaState,
  AttributeType,
  CreatorTabTypes,
  DocumentType,
  FTANodeType,
  LoaderTabTypes,
  ModelShareType,
  ModelType,
  OrganizationTabTypes,
  MemberRole,
  ProjectTableTabTypes,
  SafetyCaseType,
  SearchMode,
  SearchSelectOption,
  SelectOption,
  SettingsTabTypes,
  TraceCountTypes,
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
export function createEnumOption<T extends string>(
  enumValue: T,
  name?: string
): SelectOption {
  return { id: enumValue, name: name || enumToDisplay(enumValue) };
}

/**
 * @return display names for each document type.
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
 * @return display names for each safety case type.
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
 * @return display names for each logic type.
 */
export function logicTypeOptions(): SelectOption[] {
  return [createEnumOption(FTANodeType.AND), createEnumOption(FTANodeType.OR)];
}

/**
 * @return display names for each delta type.
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
 * @return display names for each trace count type.
 */
export function traceCountOptions(): SelectOption[] {
  return [
    createEnumOption(TraceCountTypes.all, "All Artifacts"),
    createEnumOption(TraceCountTypes.onlyTraced, "Only Traced Artifacts"),
    createEnumOption(TraceCountTypes.notTraced, "Only Orphan Artifacts"),
  ];
}

/**
 * @return display names for each approval type.
 */
export function approvalTypeOptions(): SelectOption[] {
  return [
    createEnumOption(ApprovalType.UNREVIEWED),
    createEnumOption(ApprovalType.APPROVED),
    createEnumOption(ApprovalType.DECLINED),
  ];
}

/**
 * @return display names for each trace model type.
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
 * @return display names for member role types.
 */
export function memberRoleOptions(): SelectOption[] {
  return [
    createEnumOption<MemberRole>("VIEWER", "View project data"),
    createEnumOption<MemberRole>(
      "EDITOR",
      "Edit data within a project version"
    ),
    createEnumOption<MemberRole>(
      "ADMIN",
      "Manage project versions and metadata"
    ),
    createEnumOption<MemberRole>("OWNER", "Full ownership of the project"),
  ];
}

/**
 * @return display names for model share options.
 */
export function modelShareOptions(): SelectOption[] {
  return [
    createEnumOption(ModelShareType.CLONE, "Clone the model"),
    createEnumOption(ModelShareType.REUSE, "Reuse the same model"),
  ];
}

/**
 * @return display names for project creator tabs.
 */
export function creatorTabOptions(): SelectOption[] {
  return [
    createEnumOption(CreatorTabTypes.standard, "Standard Upload"),
    createEnumOption(CreatorTabTypes.bulk, "Bulk Upload"),
    createEnumOption(CreatorTabTypes.import, "Integrations Import"),
  ];
}

/**
 * @return display names for project loader tabs.
 */
export function loaderTabOptions(): SelectOption[] {
  return [
    createEnumOption(LoaderTabTypes.load, "Open Project"),
    createEnumOption(LoaderTabTypes.uploads, "Project Uploads"),
  ];
}

/**
 * @return display names for trace prediction tabs.
 */
export function tracePredictionTabOptions(): SelectOption[] {
  return [
    createEnumOption(TracePredictionTabTypes.models, "Models"),
    createEnumOption(TracePredictionTabTypes.generation, "Trace Generation"),
    createEnumOption(TracePredictionTabTypes.approval, "Trace Approval"),
  ];
}

/**
 * @return display names for project settings tabs.
 */
export function settingsTabOptions(): SelectOption[] {
  return [
    createEnumOption(SettingsTabTypes.members, "Members"),
    createEnumOption(SettingsTabTypes.upload, "Data Upload"),
    createEnumOption(SettingsTabTypes.integrations, "Data Integrations"),
    createEnumOption(SettingsTabTypes.attributes, "Custom Attributes"),
  ];
}

/**
 * @return display names for model training tabs.
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
 * @return display names for table view tabs.
 */
export function tableViewTabOptions(): SelectOption[] {
  return [
    createEnumOption(ProjectTableTabTypes.artifact, "Artifacts"),
    createEnumOption(ProjectTableTabTypes.trace, "Trace Links"),
    createEnumOption(ProjectTableTabTypes.approve, "Trace Approval"),
  ];
}

/**
 * @return display names for attribute types.
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

/**
 * @return display names for search modes.
 */
export function searchModeOptions(): SearchSelectOption[] {
  return [
    {
      id: SearchMode.prompt,
      name: "Prompt",
      description: "Find artifacts that match a search prompt",
      placeholder: "Enter a prompt...",
    },
    {
      id: SearchMode.artifacts,
      name: "Artifact",
      description: "Find artifacts related to a specific artifact",
      placeholder: "Search artifacts...",
      artifactSearch: true,
    },
    {
      id: SearchMode.search,
      name: "Basic",
      description: "Search through currently displayed artifacts",
      placeholder: "Search current artifacts...",
      artifactSearch: true,
    },
  ];
}

/**
 * @return display names for organizations tabs.
 */
export function organizationTabTypes(): SelectOption[] {
  return [
    createEnumOption(OrganizationTabTypes.members, "Members"),
    createEnumOption(OrganizationTabTypes.teams, "Teams"),
  ];
}
