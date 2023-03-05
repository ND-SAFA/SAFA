import { FlatTraceLink, TableColumn } from "@/types";

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
  {
    name: "actions",
    label: "Actions",
    field: () => "",
  },
];
