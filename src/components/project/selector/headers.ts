import { IdentifierSchema, TableColumn } from "@/types";

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
  {
    name: "actions",
    label: "Actions",
    sortable: false,
    field: () => "",
  },
];
