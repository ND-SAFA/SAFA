import { IdentifierSchema, TableColumn, VersionSchema } from "@/types";

export const actionColumn = {
  name: "actions",
  label: "Actions",
  sortable: false,
  field: (): string => "",
};

export const projectNameColumn: TableColumn<IdentifierSchema> = {
  name: "name",
  label: "Name",
  sortable: true,
  field: (row) => row.name,
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
  actionColumn,
];

export const versionColumns: TableColumn<VersionSchema>[] = [
  {
    name: "majorVersion",
    label: "Major",
    sortable: true,
    field: (row) => row.majorVersion,
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
