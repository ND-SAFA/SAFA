import { InstallationSchema, TableColumn } from "@/types";

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
  },
  {
    label: "Actions",
    name: "actions",
    field: () => "",
  },
];
