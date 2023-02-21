<template>
  <data-table
    v-model:selected="selectedRows"
    :columns="props.columns"
    :rows="props.rows"
    :row-key="rowKey"
    selection="single"
    data-cy="generic-selector-table"
    @row-click="handleRowClick"
  >
    <template #selection>
      <div />
    </template>
  </data-table>
</template>

<script lang="ts">
/**
 * A data table for selecting items.
 */
export default {
  name: "SelectorTable",
};
</script>

<script setup lang="ts">
import { TableColumn } from "@/types";
import { useVModel } from "@/hooks";
import DataTable from "./DataTable.vue";

const props = defineProps<{
  /**
   * Whether to display loading state.
   */
  loading?: boolean;
  /**
   * The columns to render in the table.
   */
  columns: TableColumn[];
  /**
   * The rows of the table.
   */
  rows: Record<string, unknown>;
  /**
   * The field on each row that is unique.
   */
  rowKey: string | ((row: Record<string, unknown>) => string);
  /**
   * The values of selected rows.
   */
  selected: Record<string, unknown>[];
}>();

const emit = defineEmits<{
  (e: "update:selected", rows: Record<string, unknown>[]): void;
}>();

const selectedRows = useVModel(props, "selected");

/**
 * Selects a clicked row, or deselects a selected row.
 * @param evt - The click event.
 * @param row - The row to toggle selecting.
 */
function handleRowClick(evt: Event, row: Record<string, unknown>): void {
  if (props.selected.includes(row)) {
    emit("update:selected", []);
  } else {
    emit("update:selected", [row]);
  }
}
</script>
