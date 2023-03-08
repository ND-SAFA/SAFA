import {
  ArtifactSchema,
  AttributeSchema,
  FlatArtifact,
  FlatTraceLink,
  GenerationModelSchema,
  IdentifierSchema,
  InstallationSchema,
  JobSchema,
  MembershipSchema,
  TableColumn,
  VersionSchema,
} from "@/types";
import { timestampToDisplay } from "@/util/string-helper";

export const actionsColumn: TableColumn<
  | FlatArtifact
  | FlatTraceLink
  | IdentifierSchema
  | VersionSchema
  | InstallationSchema
  | GenerationModelSchema
  | MembershipSchema
> = {
  name: "actions",
  label: "Actions",
  field: () => "",
  sortable: false,
};

export const artifactColumns: TableColumn<FlatArtifact>[] = [
  {
    name: "name",
    label: "Name",
    field: (row) => row.name,
    sortable: true,
    align: "left",
  },
  {
    name: "type",
    label: "Type",
    field: (row) => row.type,
    sortable: true,
  },
];

export const artifactDeltaColumn: TableColumn<FlatArtifact> = {
  name: "deltaType",
  label: "Delta State",
  field: () => "",
  sortable: true,
};

export const artifactAttributesColumns: (
  attributes: AttributeSchema[]
) => TableColumn<FlatArtifact>[] = (attributes) =>
  attributes.map(({ key, label }) => ({
    label,
    name: key,
    field: (row: FlatArtifact) => (row[key] === undefined ? "" : row[key]),
    sortable: true,
  }));

export const artifactMatrixColumns: (
  artifacts: ArtifactSchema[]
) => TableColumn<FlatArtifact>[] = (attributes) =>
  attributes.map(({ id, name }) => ({
    label: name,
    name: id,
    field: () => "",
    sortable: true,
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
    label: "Progress",
    field: (job) => job.currentProgress,
  },
  {
    name: "status",
    label: "Status",
    field: (job) => job.status,
  },
];

export const approvalColumns: TableColumn<FlatTraceLink>[] = [
  {
    name: "sourceName",
    label: "Source Name",
    field: (row) => row.sourceName,
    sortable: true,
  },
  {
    name: "sourceType",
    label: "Source Type",
    field: (row) => row.sourceType,
    sortable: true,
  },
  {
    name: "targetName",
    label: "Target Name",
    field: (row) => row.targetName,
    sortable: true,
  },
  {
    name: "targetType",
    label: "Target Type",
    field: (row) => row.targetType,
    sortable: true,
  },
  {
    name: "approvalStatus",
    label: "Approval Status",
    field: (row) => row.approvalStatus,
    sortable: true,
  },
  {
    name: "score",
    label: "Confidence Score",
    field: (row) => row.score,
    sortable: true,
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
    field: (row) => row.installationId,
  },
  {
    label: "Last Synced",
    name: "lastUpdate",
    field: (row) => row.lastUpdate,
    format: (lastUpdate: string) => timestampToDisplay(lastUpdate),
  },
  actionsColumn,
];

export const modelColumns: TableColumn<GenerationModelSchema>[] = [
  {
    name: "name",
    label: "Name",
    field: (row) => row.name,
    align: "left",
  },
  {
    name: "baseModel",
    label: "Base Model",
    field: (row) => row.baseModel,
  },
  actionsColumn,
];

export const projectNameColumn: TableColumn<IdentifierSchema> = {
  name: "name",
  label: "Name",
  sortable: true,
  field: (row) => row.name,
  align: "left",
};

export const projectExpandedColumns: TableColumn<IdentifierSchema>[] = [
  {
    name: "description",
    label: "Description",
    sortable: false,
    field: (row) => row.description,
  },
  {
    name: "owner",
    label: "Owner",
    sortable: false,
    field: (row) => row.owner,
  },
  actionsColumn,
];

export const versionColumns: TableColumn<VersionSchema>[] = [
  {
    name: "majorVersion",
    label: "Major",
    sortable: true,
    field: (row) => row.majorVersion,
    align: "left",
  },
  {
    name: "minorVersion",
    label: "Minor",
    sortable: true,
    field: (row) => row.minorVersion,
  },
  {
    name: "revision",
    label: "Revision",
    sortable: true,
    field: (row) => row.revision,
  },
];

export const membersColumns: TableColumn<MembershipSchema>[] = [
  {
    label: "Email",
    name: "email",
    field: (row) => row.email,
    align: "left",
  },
  {
    label: "Role",
    name: "role",
    field: (row) => row.role,
  },
  actionsColumn,
];
