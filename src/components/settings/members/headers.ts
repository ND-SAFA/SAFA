import { MembershipSchema, TableColumn } from "@/types";

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
  {
    label: "Actions",
    name: "actions",
    field: (row) => "",
    sortable: false,
  },
];
