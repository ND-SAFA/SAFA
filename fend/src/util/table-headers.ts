import {
  ArtifactSchema,
  AttributeSchema,
  FlatArtifact,
  FlatTraceLink,
  IdentifierSchema,
  InstallationSchema,
  JobSchema,
  MembershipSchema,
  TableColumn,
  TransactionSchema,
  VersionSchema,
} from "@/types";
import { timestampToDisplay } from "@/util/string-helper";

export const actionsColumn: TableColumn<
  | FlatArtifact
  | FlatTraceLink
  | IdentifierSchema
  | VersionSchema
  | InstallationSchema
  | MembershipSchema
  | Record<string, string>
> = {
  name: "actions",
  label: "Actions",
  sortable: false,
  align: "right",
  field: () => "",
};

export const artifactColumns: TableColumn<FlatArtifact>[] = [
  {
    name: "name",
    label: "Name",
    sortable: true,
    align: "left",
    classes: "data-table-cell-200",
    field: (row) => row.name,
  },
  {
    name: "type",
    label: "Type",
    sortable: true,
    align: "right",
    classes: "data-table-cell-200",
    field: (row) => row.type,
  },
];

export const artifactDeltaColumn: TableColumn<FlatArtifact> = {
  name: "deltaType",
  label: "Delta State",
  sortable: true,
  align: "right",
  classes: "data-table-cell-200",
  field: () => "",
};

export const artifactAttributesColumns: (
  attributes: AttributeSchema[]
) => TableColumn<FlatArtifact>[] = (attributes) =>
  attributes.map(({ key, label }) => ({
    label,
    name: key,
    field: (row: FlatArtifact) => (row[key] === undefined ? "" : row[key]),
    sortable: true,
    groupable: false,
    align: "right",
    classes: "data-table-cell-200",
  }));

export const artifactMatrixColumns: (
  artifacts: ArtifactSchema[]
) => TableColumn<FlatArtifact>[] = (attributes) =>
  attributes.map(({ id, name }) => ({
    label: name,
    name: id,
    field: () => "",
    sortable: true,
    align: "right",
  }));

export const jobColumns: TableColumn<JobSchema>[] = [
  {
    name: "name",
    label: "Name",
    field: (job) => job.name,
    align: "left",
  },
  {
    name: "currentProgress",
    label: "Last Updated",
    align: "right",
    field: (job) => job.currentProgress,
  },
  {
    name: "duration",
    label: "Duration",
    align: "right",
    field: () => "",
  },
  {
    name: "status",
    label: "Status",
    align: "right",
    field: (job) => job.status,
  },
];

export const approvalColumns: TableColumn<FlatTraceLink>[] = [
  {
    name: "sourceName",
    label: "Child Name",
    field: (row) => row.sourceName,
    sortable: true,
    align: "left",
  },
  {
    name: "sourceType",
    label: "Child Type",
    field: (row) => row.sourceType,
    sortable: true,
    align: "right",
  },
  {
    name: "targetName",
    label: "Parent Name",
    field: (row) => row.targetName,
    sortable: true,
    align: "right",
  },
  {
    name: "targetType",
    label: "Parent Type",
    field: (row) => row.targetType,
    sortable: true,
    align: "right",
  },
  {
    name: "approvalStatus",
    label: "Approval Status",
    field: (row) => row.approvalStatus,
    sortable: true,
    align: "right",
  },
  {
    name: "score",
    label: "Confidence Score",
    field: (row) => row.score,
    sortable: true,
    align: "right",
  },
  actionsColumn,
];

export const installationsColumns: TableColumn<InstallationSchema>[] = [
  {
    label: "Integration Type",
    name: "type",
    field: (row) => row.type,
    align: "left",
  },
  {
    label: "Project ID",
    name: "installationId",
    align: "right",
    field: (row) => row.installationId,
  },
  {
    label: "Last Synced",
    name: "lastUpdate",
    align: "right",
    field: (row) => row.lastUpdate,
    format: (lastUpdate: string) => timestampToDisplay(lastUpdate),
  },
  actionsColumn,
];

export const projectNameColumn: TableColumn<IdentifierSchema> = {
  name: "name",
  label: "Name",
  sortable: true,
  align: "left",
  classes: "data-table-cell-200",
  field: (row) => row.name,
};

export const projectColumns: TableColumn<IdentifierSchema>[] = [
  projectNameColumn,
  actionsColumn,
];

export const versionColumns: TableColumn<VersionSchema>[] = [
  {
    name: "majorVersion",
    label: "Major",
    sortable: true,
    align: "left",
    field: (row) => row.majorVersion,
  },
  {
    name: "minorVersion",
    label: "Minor",
    sortable: true,
    align: "left",
    field: (row) => row.minorVersion,
  },
  {
    name: "revision",
    label: "Revision",
    sortable: true,
    align: "left",
    field: (row) => row.revision,
  },
];

export const membersColumns: TableColumn<MembershipSchema>[] = [
  {
    label: "Email",
    name: "email",
    align: "left",
    field: (row) => row.email,
  },
  {
    label: "Role",
    name: "role",
    align: "right",
    field: (row) => row.role,
  },
  actionsColumn,
];

export const teamColumns: TableColumn<Record<string, string>>[] = [
  {
    label: "Name",
    name: "name",
    align: "left",
    field: (row) => row.name,
  },
  {
    label: "Members",
    name: "members",
    align: "right",
    field: (row) => row.members.length,
  },
  {
    label: "Projects",
    name: "projects",
    align: "right",
    field: (row) => row.projects.length,
  },
  actionsColumn,
];

export const transactionsColumns: TableColumn<TransactionSchema>[] = [
  {
    label: "Description",
    name: "description",
    align: "left",
    field: (row) => row.description,
  },
  {
    label: "Status",
    name: "status",
    align: "right",
    field: (row) => row.status,
  },
  {
    label: "Amount",
    name: "amount",
    align: "right",
    field: (row) => `$${row.amount}`,
  },
  {
    label: "Date",
    name: "timestamp",
    align: "right",
    field: (row) => row.timestamp,
    format: (timestamp: string) => timestampToDisplay(timestamp),
  },
];
