import { GenerationModelSchema, TableColumn } from "@/types";

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
  {
    name: "actions",
    label: "Actions",
    field: () => "",
  },
];
