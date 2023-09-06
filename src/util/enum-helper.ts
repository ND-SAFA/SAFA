import {
  ApprovalType,
  ArtifactDeltaState,
  AttributeType,
  CreatorTabTypes,
  DocumentType,
  FTANodeType,
  LoaderTabTypes,
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
  MembershipType,
  TeamTabTypes,
} from "@/types";
import { enumToDisplay } from "@/util/string-helper";

/**
 * Converts an enum value into a selectable option with a title case name.
 *
 * @param enumValue - The enum value in upper snake case to convert.
 * @param name - The name of the option, which will bne generated if not given.
 * @return The selectable option.
 */
export function createOption<T extends string>(
  enumValue: T,
  name?: string
): SelectOption<T> {
  return { id: enumValue, name: name || enumToDisplay(enumValue) };
}

/**
 * @return display names for each document type.
 */
export function documentTypeOptions(): SelectOption[] {
  return [
    createOption(DocumentType.ARTIFACT_TREE, "Default"),
    createOption(DocumentType.FTA, "FTA"),
    createOption(DocumentType.SAFETY_CASE),
    createOption(DocumentType.FMEA, "FMEA"),
    createOption(DocumentType.FMECA, "FMECA"),
  ];
}

/**
 * @return display names for each safety case type.
 */
export function safetyCaseOptions(): SelectOption[] {
  return [
    createOption(SafetyCaseType.CONTEXT),
    createOption(SafetyCaseType.GOAL),
    createOption(SafetyCaseType.STRATEGY),
    createOption(SafetyCaseType.SOLUTION),
  ];
}

/**
 * @return display names for each logic type.
 */
export function logicTypeOptions(): SelectOption[] {
  return [createOption(FTANodeType.AND), createOption(FTANodeType.OR)];
}

/**
 * @return display names for each delta type.
 */
export function deltaTypeOptions(): SelectOption[] {
  return [
    createOption(ArtifactDeltaState.NO_CHANGE),
    createOption(ArtifactDeltaState.ADDED),
    createOption(ArtifactDeltaState.MODIFIED),
    createOption(ArtifactDeltaState.REMOVED),
  ];
}

/**
 * @return display names for each trace count type.
 */
export function traceCountOptions(): SelectOption[] {
  return [
    createOption(TraceCountTypes.all, "All Artifacts"),
    createOption(TraceCountTypes.onlyTraced, "Only Traced Artifacts"),
    createOption(TraceCountTypes.notTraced, "Only Orphan Artifacts"),
  ];
}

/**
 * @return display names for each approval type.
 */
export function approvalTypeOptions(): SelectOption[] {
  return [
    createOption(ApprovalType.UNREVIEWED),
    createOption(ApprovalType.APPROVED),
    createOption(ApprovalType.DECLINED),
  ];
}

/**
 * @param type - The type of member roles to include.
 * @return display names for member role types.
 */
export function memberRoleOptions(type?: MembershipType): SelectOption[] {
  const roles: SelectOption<MemberRole>[] = [];

  // Include the given role if the type matches or if no type is given.
  const addRoleFor = (
    matchTypes: MembershipType[],
    role: MemberRole,
    description: string
  ) =>
    (matchTypes.length === 0 || matchTypes.includes(type || "PROJECT")) &&
    roles.push(createOption(role, description));

  addRoleFor(["PROJECT", "TEAM"], "VIEWER", "View project data");
  addRoleFor(
    ["PROJECT", "TEAM"],
    "EDITOR",
    "Edit data within a project version"
  );
  addRoleFor([], "GENERATOR", "Use generative features on project data");
  addRoleFor([], "ADMIN", "Manage projects and membership");
  addRoleFor(["PROJECT"], "OWNER", "Full ownership of the project");
  addRoleFor(["ORGANIZATION"], "MEMBER", "A member of the organization");
  addRoleFor(
    ["ORGANIZATION"],
    "BILLING_MANAGER",
    "Manage billing for the organization"
  );

  return roles;
}

/**
 * @return display names for project creator tabs.
 */
export function creatorTabOptions(): SelectOption[] {
  return [
    createOption(CreatorTabTypes.standard, "Standard Upload"),
    createOption(CreatorTabTypes.bulk, "Bulk Upload"),
    createOption(CreatorTabTypes.import, "Integrations Import"),
  ];
}

/**
 * @return display names for project loader tabs.
 */
export function loaderTabOptions(): SelectOption[] {
  return [
    createOption(LoaderTabTypes.load, "Open Project"),
    createOption(LoaderTabTypes.uploads, "Project Uploads"),
  ];
}

/**
 * @return display names for trace prediction tabs.
 */
export function tracePredictionTabOptions(): SelectOption[] {
  return [
    createOption(TracePredictionTabTypes.models, "Models"),
    createOption(TracePredictionTabTypes.generation, "Trace Generation"),
    createOption(TracePredictionTabTypes.approval, "Trace Approval"),
  ];
}

/**
 * @return display names for project settings tabs.
 */
export function settingsTabOptions(): SelectOption[] {
  return [
    createOption(SettingsTabTypes.members, "Members"),
    createOption(SettingsTabTypes.upload, "Data Upload"),
    createOption(SettingsTabTypes.integrations, "Data Integrations"),
    createOption(SettingsTabTypes.attributes, "Custom Attributes"),
  ];
}

/**
 * @return display names for table view tabs.
 */
export function tableViewTabOptions(): SelectOption[] {
  return [
    createOption(ProjectTableTabTypes.artifact, "Artifacts"),
    createOption(ProjectTableTabTypes.trace, "Trace Links"),
    createOption(ProjectTableTabTypes.approve, "Trace Approval"),
  ];
}

/**
 * @return display names for attribute types.
 */
export function attributeTypeOptions(): SelectOption[] {
  return [
    createOption(AttributeType.text, "Text"),
    createOption(AttributeType.paragraph, "Paragraph"),
    createOption(AttributeType.select, "Select"),
    createOption(AttributeType.multiselect, "Multiselect"),
    createOption(AttributeType.relation, "Relation"),
    createOption(AttributeType.date, "Date"),
    createOption(AttributeType.int, "Integer"),
    createOption(AttributeType.float, "Number"),
    createOption(AttributeType.boolean, "Yes/No"),
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
 * @return display names for organization tabs.
 */
export function organizationTabTypes(): SelectOption[] {
  return [
    createOption(OrganizationTabTypes.members, "Members"),
    createOption(OrganizationTabTypes.teams, "Teams"),
  ];
}

/**
 * @return display names for team tabs.
 */
export function teamTabTypes(): SelectOption[] {
  return [
    createOption(TeamTabTypes.members, "Members"),
    createOption(TeamTabTypes.projects, "Projects"),
  ];
}
