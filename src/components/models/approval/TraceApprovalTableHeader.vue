<template>
  <table-header
    v-model:group-by="groupBy"
    v-model:sort-by="sortBy"
    v-model:sort-desc="sortDesc"
    v-model:group-desc="groupDesc"
    v-model:search-text="searchText"
    show-commit-buttons
    :headers="headers"
  >
    <template #right>
      <flex-box>
        <v-divider vertical />
        <v-autocomplete
          v-model="approvalTypes"
          outlined
          dense
          hide-details
          multiple
          label="Approval Types"
          :items="options"
          item-text="name"
          item-value="id"
          class="ml-2"
          data-cy="button-trace-link-generate-approval-type"
        />
      </flex-box>
    </template>
    <template #bottom>
      <text-button
        text
        color="error"
        icon-id="mdi-close-circle-multiple-outline"
        @click="handleDeclineAll"
      >
        Clear Unreviewed
      </text-button>
    </template>
  </table-header>
</template>

<script lang="ts">
/**
 * Displays the header for the trace approval table.
 */
export default {
  name: "TraceApprovalTableHeader",
};
</script>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";
import { DataTableHeader, FlatTraceLink } from "@/types";
import { approvalTypeOptions } from "@/util";
import { useVModel } from "@/hooks";
import { handleDeclineAll } from "@/api";
import { TableHeader, TextButton, FlexBox } from "@/components/common";

const props = defineProps<{
  headers: DataTableHeader<FlatTraceLink>[];
  searchText: string;
  groupBy: string;
  sortBy: string[];
  groupDesc: boolean;
  sortDesc: boolean;
  approvalTypes: string[];
}>();

const emit = defineEmits<{
  (e: "update:searchText", text: string): void;
  (e: "update:sortBy", values: string[]): void;
  (e: "update:sortDesc", descending: boolean): void;
  (e: "update:groupBy", value: string): void;
  (e: "update:groupDesc", descending: boolean): void;
  (e: "update:approvalTypes", types: string[]): void;
}>();

const options = approvalTypeOptions();
const searchText = useVModel(props, "searchText");
const sortBy = useVModel(props, "sortBy");
const sortDesc = useVModel(props, "sortDesc");
const groupBy = useVModel(props, "groupBy");
const groupDesc = useVModel(props, "groupDesc");
const approvalTypes = useVModel(props, "approvalTypes");
</script>
