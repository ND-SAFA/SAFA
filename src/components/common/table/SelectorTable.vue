<template>
  <data-table
    v-model:sort-by="sortBy"
    v-model:sort-desc="sortDesc"
    v-model:selected="selectedRows"
    :columns="props.columns"
    :rows="filteredRows"
    :row-key="props.rowKey"
    :rows-per-page="5"
    :loading="props.loading"
    selection="single"
    data-cy="generic-selector-table"
    :custom-cells="['actions']"
    :sort="(r) => r"
    @row-click="handleRowClick"
  >
    <template #selection>
      <div />
    </template>

    <template v-if="!props.minimal" #top>
      <flex-box full-width align="center" justify="between" y="2">
        <searchbar v-model="searchText" :label="searchLabel" />
        <icon-button
          tooltip="Refresh"
          icon="graph-refresh"
          data-cy="button-selector-reload"
          class="q-ml-sm"
          @click="emit('refresh')"
        />
      </flex-box>
    </template>

    <template #body-cell-actions="{ row }">
      <q-td @click.stop="">
        <flex-box justify="end">
          <slot name="cell-actions" :row="row" />
          <icon-button
            v-if="isEditEnabled(row)"
            icon="edit"
            :tooltip="editLabel"
            data-cy="button-selector-edit"
            @click="$emit('row:edit', row)"
          />
          <icon-button
            v-if="isDeleteEnabled(row)"
            icon="delete"
            :tooltip="deleteLabel"
            data-cy="button-selector-delete"
            @click="$emit('row:delete', row)"
          />
        </flex-box>
      </q-td>
    </template>

    <template v-if="!props.minimal && props.addable" #bottom>
      <icon-button
        fab
        color="primary"
        icon="add"
        :tooltip="addLabel"
        data-cy="button-selector-add"
        @click="$emit('row:add')"
      />
      <slot name="bottom" />
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
import { computed } from "vue";
import { TableColumn, TableRow } from "@/types";
import { useTableFilter, useVModel } from "@/hooks";
import { FlexBox } from "@/components/common/layout";
import { Searchbar } from "@/components/common/input";
import { IconButton } from "@/components/common/button";
import DataTable from "./DataTable.vue";

const props = defineProps<{
  /**
   * The columns to render in the table.
   */
  columns: TableColumn[];
  /**
   * The rows of the table.
   */
  rows: TableRow[];
  /**
   * The field on each row that is unique.
   */
  rowKey: string | ((row: TableRow) => string);
  /**
   * Whether to display loading state.
   */
  loading?: boolean;
  /**
   * The values of selected rows.
   */
  selected?: TableRow[];
  /**
   * The name of an item.
   */
  itemName?: string;
  /**
   * Whether elements can be added.
   */
  addable?: boolean;
  /**
   * Whether these rows are editable.
   */
  editable?: boolean | ((row: TableRow) => boolean);
  /**
   * Whether these rows are deletable.
   */
  deletable?: boolean | ((row: TableRow) => boolean);
  /**
   * Whether to display minimal information.
   */
  minimal?: boolean;
}>();

const emit = defineEmits<{
  (e: "update:selected", rows: TableRow[]): void;
  (e: "refresh"): void;
  (e: "row:edit", row: TableRow): void;
  (e: "row:delete", row: TableRow): void;
  (e: "row:add"): void;
}>();

const selectedRows = useVModel(props, "selected");

const { searchText, searchLabel, sortBy, sortDesc, filteredRows } =
  useTableFilter(props);

const addLabel = computed(() => `Add ${props.itemName || ""}`);
const editLabel = computed(() => `Edit ${props.itemName || ""}`);
const deleteLabel = computed(() => `Delete ${props.itemName || ""}`);

/**
 * Selects a clicked row, or deselects a selected row.
 * @param evt - The click event.
 * @param row - The row to toggle selecting.
 */
function handleRowClick(evt: Event, row: TableRow): void {
  if (props.selected?.includes(row)) {
    emit("update:selected", []);
  } else {
    emit("update:selected", [row]);
  }
}

/**
 * Whether a row can be edited.
 * @param row - The row to check.
 * @return Whether it is editable.
 */
function isEditEnabled(row: TableRow): boolean {
  return typeof props.editable === "function"
    ? props.editable(row)
    : !!props.editable;
}

/**
 * Whether a row can be deleted.
 * @param row - The row to check.
 * @return Whether it is deletable.
 */
function isDeleteEnabled(row: TableRow): boolean {
  return typeof props.deletable === "function"
    ? props.deletable(row)
    : !!props.deletable;
}
</script>
