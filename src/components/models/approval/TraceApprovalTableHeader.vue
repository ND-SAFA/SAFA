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
      </fle>
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
import { defineProps, defineEmits, ref, watch } from "vue";
import { DataTableHeader, FlatTraceLink } from "@/types";
import { approvalTypeOptions } from "@/util";
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
const searchText = ref(props.searchText);
const sortBy = ref(props.sortBy);
const sortDesc = ref(props.sortDesc);
const groupBy = ref(props.groupBy);
const groupDesc = ref(props.groupDesc);
const approvalTypes = ref(props.approvalTypes);

watch(
  () => searchText.value,
  () => emit("update:searchText", searchText.value)
);

watch(
  () => sortBy.value,
  () => emit("update:sortBy", sortBy.value)
);

watch(
  () => sortDesc.value,
  () => emit("update:sortDesc", sortDesc.value)
);

watch(
  () => groupBy.value,
  () => emit("update:groupBy", groupBy.value)
);

watch(
  () => groupDesc.value,
  () => emit("update:groupDesc", groupDesc.value)
);

watch(
  () => approvalTypes.value,
  () => emit("update:approvalTypes", approvalTypes.value)
);
</script>
