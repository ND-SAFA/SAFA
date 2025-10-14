import {
  ApprovalType,
  ArtifactDeltaState,
  AttributeType,
  CreatorSectionTab,
  LoaderTab,
  MemberRole,
  MembershipType,
  OrganizationTabTypes,
  ProjectOwnerType,
  ProjectTableTab,
  SearchSelectOption,
  SelectOption,
  SettingsTab,
  TeamTabTypes,
  TraceCountTypes,
  UploadPanelType,
} from "@/types";
import { enumToDisplay } from "@/util/string-helper";
import { ENABLED_FEATURES } from "@/util/enabled-features";

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
 * @return display names for each delta type.
 */
export function deltaTypeOptions(): SelectOption<ArtifactDeltaState>[] {
  return [
    createOption("NO_CHANGE"),
    createOption("ADDED"),
    createOption("MODIFIED"),
    createOption("REMOVED"),
  ];
}

/**
 * @return display names for each trace count type.
 */
export function traceCountOptions(): SelectOption<TraceCountTypes>[] {
  return [
    createOption("all", "All Artifacts"),
    createOption("onlyTraced", "Only Traced Artifacts"),
    createOption("notTraced", "Only Orphan Artifacts"),
  ];
}

/**
 * @return display names for each approval type.
 */
export function approvalTypeOptions(): SelectOption<ApprovalType>[] {
  return [
    createOption("UNREVIEWED"),
    createOption("APPROVED"),
    createOption("DECLINED"),
  ];
}

/**
 * @param type - The type of member roles to include.
 * @return display names for member role types.
 */
export function memberRoleOptions(
  type?: MembershipType
): SelectOption<MemberRole>[] {
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
 * @return display names for attribute types.
 */
export function attributeTypeOptions(): SelectOption<AttributeType>[] {
  return [
    createOption("text", "Text"),
    createOption("paragraph", "Paragraph"),
    createOption("select", "Select"),
    createOption("multiselect", "Multiselect"),
    createOption("relation", "Relation"),
    createOption("date", "Date"),
    createOption("int", "Integer"),
    createOption("float", "Number"),
    createOption("boolean", "Yes/No"),
  ];
}

/**
 * @return display names for search modes.
 */
export function searchModeOptions(): SearchSelectOption[] {
  return [
    {
      id: "chat",
      name: "Chat",
      description: "Create a new project chat based on your search",
      placeholder: "Ask a question...",
    },
    {
      id: "prompt",
      name: "Prompt",
      description: "Find artifacts that match a search prompt",
      placeholder: "Enter a prompt...",
    },
    {
      id: "artifacts",
      name: "Artifact",
      description: "Find artifacts related to a specific artifact",
      placeholder: "Search artifacts...",
      artifactSearch: true,
    },
    {
      id: "search",
      name: "Text",
      description: "Search through currently displayed artifacts",
      placeholder: "Search current artifacts...",
      artifactSearch: true,
    },
  ];
}

/**
 * @return display names for project creator tabs.
 */
export function uploadPanelOptions(): SelectOption<UploadPanelType>[] {
  return [
    createOption("artifact", "Artifact Type"),
    createOption("trace", "Trace Matrix"),
    createOption("bulk", "Bulk File Upload"),
    createOption("github", "GitHub Upload"),
    createOption("jira", "Jira Upload"),
  ];
}

/**
 * @return display names for project owner types.
 */
export function ownerTypeOptions(): SelectOption<ProjectOwnerType>[] {
  return [
    createOption("ORGANIZATION", "Organization"),
    createOption("TEAM", "Organization Team"),
    createOption("USER_ID", "Organization Member"),
    createOption("USER_EMAIL", "User Email"),
  ];
}

/**
 * @return display names for project creator tabs.
 */
export function creatorTabOptions(): SelectOption<CreatorSectionTab>[] {
  return [createOption("name", "Details"), createOption("data", "Data")];
}

/**
 * @return display names for project loader tabs.
 */
export function loaderTabOptions(): SelectOption<LoaderTab>[] {
  return [
    createOption("load", "My Projects"),
    createOption("user", "Recent Jobs"),
    createOption("project", "Project Jobs"),
  ];
}

/**
 * @return display names for project settings tabs.
 */
export function settingsTabOptions(): SelectOption<SettingsTab>[] {
  return [
    createOption("overview", "Overview"),
    createOption("members", "Members"),
    createOption("jobs", "Jobs"),
    createOption("upload", "Data Upload"),
    createOption("integrations", "Data Integrations"),
    createOption("attributes", "Custom Attributes"),
  ];
}

/**
 * @return display names for table view tabs.
 */
export function tableViewTabOptions(): SelectOption<ProjectTableTab>[] {
  return [
    createOption("artifact", "Artifacts"),
    createOption("trace", "Trace Links"),
    ...(ENABLED_FEATURES.TRACE_MATRIX_TABLE
      ? [createOption("matrix", "Trace Matrix")]
      : []),
  ];
}

/**
 * @return display names for organization tabs.
 */
export function organizationTabTypes(): SelectOption<OrganizationTabTypes>[] {
  return [
    createOption("members", "Members"),
    createOption("teams", "Teams"),
    createOption("billing", "Transactions"),
  ];
}

/**
 * @return display names for team tabs.
 */
export function teamTabTypes(): SelectOption<TeamTabTypes>[] {
  return [
    createOption("members", "Members"),
    createOption("projects", "Projects"),
  ];
}
