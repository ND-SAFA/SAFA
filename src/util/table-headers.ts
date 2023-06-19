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
  align: "left",
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
    align: "left",
  },
];

export const artifactDeltaColumn: TableColumn<FlatArtifact> = {
  name: "deltaType",
  label: "Delta State",
  field: () => "",
  sortable: true,
  align: "left",
};

export const artifactAttributesColumns: (
  attributes: AttributeSchema[]
) => TableColumn<FlatArtifact>[] = (attributes) =>
  attributes.map(({ key, label }) => ({
    label,
    name: key,
    field: (row: FlatArtifact) => (row[key] === undefined ? "" : row[key]),
    sortable: true,
    align: "left",
  }));

export const artifactMatrixColumns: (
  artifacts: ArtifactSchema[]
) => TableColumn<FlatArtifact>[] = (attributes) =>
  attributes.map(({ id, name }) => ({
    label: name,
    name: id,
    field: () => "",
    sortable: true,
    align: "left",
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
    align: "left",
    field: (job) => job.currentProgress,
  },
  {
    name: "status",
    label: "Status",
    align: "left",
    field: (job) => job.status,
  },
];

export const approvalColumns: TableColumn<FlatTraceLink>[] = [
  {
    name: "sourceName",
    label: "Source Name",
    field: (row) => row.sourceName,
    sortable: true,
    align: "left",
  },
  {
    name: "sourceType",
    label: "Source Type",
    field: (row) => row.sourceType,
    sortable: true,
    align: "left",
  },
  {
    name: "targetName",
    label: "Target Name",
    field: (row) => row.targetName,
    sortable: true,
    align: "left",
  },
  {
    name: "targetType",
    label: "Target Type",
    field: (row) => row.targetType,
    sortable: true,
    align: "left",
  },
  {
    name: "approvalStatus",
    label: "Approval Status",
    field: (row) => row.approvalStatus,
    sortable: true,
    align: "left",
  },
  {
    name: "score",
    label: "Confidence Score",
    field: (row) => row.score,
    sortable: true,
    align: "left",
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
    align: "left",
    field: (row) => row.installationId,
  },
  {
    label: "Last Synced",
    name: "lastUpdate",
    align: "left",
    field: (row) => row.lastUpdate,
    format: (lastUpdate: string) => timestampToDisplay(lastUpdate),
  },
  actionsColumn,
];

export const modelColumns: TableColumn<GenerationModelSchema>[] = [
  {
    name: "name",
    label: "Name",
    align: "left",
    field: (row) => row.name,
  },
  {
    name: "baseModel",
    label: "Base Model",
    align: "left",
    field: (row) => row.baseModel,
  },
  actionsColumn,
];

export const projectNameColumn: TableColumn<IdentifierSchema> = {
  name: "name",
  label: "Name",
  sortable: true,
  align: "left",
  field: (row) => row.name,
};

export const projectExpandedColumns: TableColumn<IdentifierSchema>[] = [
  {
    name: "description",
    label: "Description",
    sortable: false,
    align: "left",
    field: (row) => row.description,
  },
  {
    name: "owner",
    label: "Owner",
    sortable: false,
    align: "left",
    field: (row) => row.owner,
  },
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
    align: "left",
    field: (row) => row.role,
  },
  actionsColumn,
];
