import { JobSchema, TableColumn } from "@/types";

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
