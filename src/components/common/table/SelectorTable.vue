<template>
  <data-table
    v-model:selected="selectedRows"
    :columns="props.columns"
    :rows="props.rows"
    :row-key="rowKey"
    :rows-per-page="5"
    selection="single"
    data-cy="generic-selector-table"
    :custom-cells="['actions']"
    @row-click="handleRowClick"
  >
    <template #selection>
      <div />
    </template>

    <template #top>
      <flex-box
        v-if="!props.minimal"
        full-width
        align="center"
        justify="between"
        y="2"
      >
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
        <flex-box>
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
      <div style="position: relative; bottom: 40px; height: 10px">
        <icon-button
          fab
          color="primary"
          icon="add"
          :tooltip="addLabel"
          data-cy="button-selector-add"
          @click="$emit('row:add')"
        />
      </div>
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
import { computed, ref } from "vue";
import { TableColumn } from "@/types";
import { useVModel } from "@/hooks";
import { FlexBox } from "@/components/common/layout";
import { Searchbar } from "@/components/common/input";
import { IconButton } from "@/components/common/button";
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
  editable?: boolean | ((row: Record<string, unknown>) => boolean);
  /**
   * Whether these rows are deletable.
   */
  deletable?: boolean | ((row: Record<string, unknown>) => boolean);
}>();

const emit = defineEmits<{
  (e: "update:selected", rows: Record<string, unknown>[]): void;
  (e: "refresh"): void;
  (e: "row:edit", row: Record<string, unknown>): void;
  (e: "row:delete", row: Record<string, unknown>): void;
  (e: "row:add"): void;
}>();

const searchText = ref("");

const selectedRows = useVModel(props, "selected");

const searchLabel = computed(() =>
  props.itemName ? `Search ${props.itemName}s` : "Search"
);
const addLabel = computed(() => `Add ${props.itemName || ""}`);
const editLabel = computed(() => `Edit ${props.itemName || ""}`);
const deleteLabel = computed(() => `Delete ${props.itemName || ""}`);

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

/**
 * Whether a row can be edited.
 * @param row - The row to check.
 * @return Whether it is editable.
 */
function isEditEnabled(row: Record<string, unknown>): boolean {
  return typeof props.editable === "function"
    ? props.editable(row)
    : !!props.editable;
}

/**
 * Whether a row can be deleted.
 * @param row - The row to check.
 * @return Whether it is deletable.
 */
function isDeleteEnabled(row: Record<string, unknown>): boolean {
  return typeof props.deletable === "function"
    ? props.deletable(row)
    : !!props.deletable;
}
</script>
