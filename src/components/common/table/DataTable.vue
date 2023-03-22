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
      :sort-method="sort"
      :separator="props.separator"
      :virtual-scroll="props.virtualScroll"
      :data-cy="props.dataCy"
      table-header-class="text-primary"
      class="data-table"
      @row-click="(e, r, i) => emit('row-click', e, r, i)"
    >
      <slot />

      <template v-if="slots.top" #top="scope">
        <slot name="top" v-bind="scope" />
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
import { TableColumn, TableRow } from "@/types";
import { sortRows } from "@/util";
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
  rows: TableRow;
  /**
   * The field on each row that is unique.
   */
  rowKey: string | ((row: TableRow) => string);
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
  selected?: TableRow[];
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
  filter?: (
    rows: TableRow[],
    filterText: string | undefined,
    cols: TableColumn[]
  ) => TableRow[];
  /**
   * Which attribute to sort by.
   */
  sortBy?: string;
  /**
   * Whether to sort descending.
   */
  sortDesc?: boolean;
  /**
   * A function to sort the table with.
   */
  sort?(rows: TableRow[], sortBy: string, descending: boolean): TableRow[];
  /**
   * Where to place separators. Defaults to horizontal.
   */
  separator?: "horizontal" | "vertical" | "cell" | "none";
  /**
   * Any cells can be customized through the slot `body-cell-[name]`.
   */
  customCells?: string[];
  /**
   * Whether to display densely.
   */
  dense?: boolean;
  /**
   * If true, virtual scroll will be enabled.
   */
  virtualScroll?: boolean;
  /**
   * The testing selector to set on this table.
   */
  dataCy?: string;
}>();

const emit = defineEmits<{
  (e: "update:selected", rows: TableRow[]): void;
  (e: "update:visibleColumns", cols: string[]): void;
  (e: "update:expanded", rows: string[]): void;
  (e: "update:sortBy", sortBy: string | undefined): void;
  (e: "row-click", evt: Event, row: TableRow, index: number): void;
}>();

const slots = useSlots();

const selectedRows = useVModel(props, "selected");
const visibleCols = useVModel(props, "visibleColumns");
const expandedRows = useVModel(props, "expanded");
const sortBy = useVModel(props, "sortBy");
const sortDesc = useVModel(props, "sortDesc");

const sort = computed(() => props.sort || sortRows);

const customCellSlots = computed(() =>
  props.customCells ? props.customCells.map((name) => `body-cell-${name}`) : []
);

const pagination = ref({
  sortBy: props.sortBy,
  descending: props.sortDesc,
  rowsPerPage: props.rowsPerPage || 20,
  page: 1,
});

watch(
  () => props.sortBy,
  (sort) => {
    if (pagination.value.sortBy === sort) return;

    pagination.value.sortBy = sort;
  }
);

watch(
  () => pagination.value.sortBy,
  (sort) => {
    if (sortBy.value === sort) return;

    sortBy.value = sort;
  }
);

watch(
  () => props.sortDesc,
  (desc) => {
    if (pagination.value.descending === desc) return;

    pagination.value.descending = desc;
  }
);

watch(
  () => pagination.value.descending,
  (desc) => {
    if (sortDesc.value === desc) return;

    sortDesc.value = desc;
  }
);
</script>
