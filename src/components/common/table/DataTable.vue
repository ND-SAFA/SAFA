<template>
  <div>
    <q-table
      v-model:expanded="expandedRows"
      v-model:selected="selectedRows"
      v-model:visible-columns="visibleCols"
      v-model:pagination="pagination"
      flat
      :dense="props.dense"
      :loading="props.loading"
      :columns="props.columns"
      :filter="props.filterText"
      :filter-method="props.filter"
      :rows="props.rows"
      :row-key="props.rowKey"
      :selection="props.selection"
      :column-sort-order="props.sortOrder"
      :sort-method="props.sort"
      :data-cy="props.dataCy"
      table-header-class="text-primary"
      @row-click="(e, r, i) => emit('row-click', e, r, i)"
    >
      <slot />

      <template v-if="slots.top" #top>
        <slot name="top" />
      </template>

      <template v-if="slots.header" #header="scope">
        <slot name="header" v-bind="scope" />
      </template>

      <template v-if="slots.body" #body="scope">
        <slot name="body" v-bind="scope" />
      </template>

      <template v-if="slots.selection" #body-selection="scope">
        <slot name="selection" v-bind="scope" />
      </template>

      <template v-if="slots.item" #item="scope">
        <slot name="item" v-bind="scope" />
      </template>

      <template v-for="name in customCellSlots" #[name]="scope">
        <slot :name="name" v-bind="scope" />
      </template>
    </q-table>
    <slot name="bottom" />
  </div>
</template>

<script lang="ts">
/**
 * A generic data table.
 */
export default {
  name: "DataTable",
};
</script>

<script setup lang="ts">
import { computed, ref, useSlots, watch } from "vue";
import { TableColumn } from "@/types";
import { useVModel } from "@/hooks";

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
   * The column names that are currently visible, if not all of them.
   */
  visibleColumns?: string[];
  /**
   * The rows of the table.
   */
  rows: Record<string, unknown>;
  /**
   * The field on each row that is unique.
   */
  rowKey: string | ((row: Record<string, unknown>) => string);
  /**
   * The number of rows to display per page.
   */
  rowsPerPage?: number;
  /**
   * Enables selection of rows.
   */
  selection?: "single" | "multiple";
  /**
   * The values of selected rows.
   */
  selected?: Record<string, unknown>[];
  /**
   * The ids of expanded rows.
   */
  expanded?: string[];
  /**
   * The text to filter by.
   */
  filterText?: string;
  /**
   * A function to filter the table with.
   */
  filter?: (rows: Record<string, unknown>[]) => Record<string, unknown>[];
  /**
   * Which attribute to sort by.
   */
  sortBy?: string;
  /**
   * Whether to sort  `ad` (ascending-descending) or `da` (descending-ascending).
   */
  sortOrder?: "ad" | "da";
  /**
   * Applies the sorting.
   * @param rows - The rows being sorted.
   * @param sortBy - The column name being sorted by.
   * @param desc - Whether sorting in descending order.
   */
  sort?: (
    rows: Record<string, unknown>[],
    sortBy: string,
    desc: boolean
  ) => Record<string, unknown>[];
  /**
   * Any cells can be customized through the slot `body-cell-[name]`.
   */
  customCells?: string[];
  /**
   * Whether to display densely.
   */
  dense?: boolean;
  /**
   * The testing selector to set on this table.
   */
  dataCy?: string;
}>();

const emit = defineEmits<{
  (e: "update:selected", rows: Record<string, unknown>[]): void;
  (e: "update:visibleColumns", cols: string[]): void;
  (e: "update:expanded", rows: string[]): void;
  (
    e: "row-click",
    evt: Event,
    row: Record<string, unknown>,
    index: number
  ): void;
}>();

const slots = useSlots();

const selectedRows = useVModel(props, "selected");
const visibleCols = useVModel(props, "visibleColumns");
const expandedRows = useVModel(props, "expanded");

const customCellSlots = computed(() =>
  props.customCells ? props.customCells.map((name) => `body-cell-${name}`) : []
);

const pagination = ref({
  sortBy: props.sortBy,
  descending: props.sortOrder === "da",
  rowsPerPage: props.rowsPerPage || 20,
  page: 1,
  rowsNumber: props.rows.length,
});

watch(
  () => props.sortBy,
  (sortBy) => (pagination.value.sortBy = sortBy)
);

watch(
  () => props.rows.length,
  (rows) => (pagination.value.rowsNumber = rows)
);

watch(
  () => props.sortBy,
  (desc) => (pagination.value.descending = desc === "da")
);
</script>
