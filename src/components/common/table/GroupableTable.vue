<template>
  <data-table
    v-model:sort-by="sortBy"
    v-model:sort-desc="sortDesc"
    v-model:expanded="expandedRows"
    :columns="props.columns"
    :rows="filteredRows"
    :row-key="props.rowKey"
    :loading="props.loading"
    :expanded="props.expandable ? expandedRows : undefined"
  >
    <template #top>
      <groupable-table-header
        v-model:search-text="searchText"
        v-model:group-by="groupBy"
        v-model:sort-by="sortBy"
        v-model:sort-desc="sortDesc"
        :columns="columns"
        :search-label="searchLabel"
      >
        <template #header-right>
          <slot name="header-right" />
        </template>
        <template #header-bottom>
          <slot name="header-bottom" />
        </template>
      </groupable-table-header>
    </template>

    <template #body="quasarProps">
      <groupable-table-row
        v-model:expand="quasarProps.expand"
        :quasar-props="quasarProps"
        :columns="props.columns"
        :row="quasarProps.row"
        :expandable="props.expandable"
      >
        <template v-for="name in customCellSlots" #[name]="scope">
          <slot :name="name" v-bind="scope" />
        </template>
        <template #body-expanded="scope">
          <slot name="body-expanded" v-bind="scope" />
        </template>
      </groupable-table-row>
    </template>
  </data-table>
</template>

<script lang="ts">
/**
 * A table that can be grouped and expanded.
 */
export default {
  name: "GroupableTable",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { TableColumn } from "@/types";
import { useTableFilter, useVModel } from "@/hooks";
import GroupableTableRow from "./GroupableTableRow.vue";
import GroupableTableHeader from "./GroupableTableHeader.vue";
import DataTable from "./DataTable.vue";

const props = defineProps<{
  /**
   * The columns to render in the table.
   */
  columns: TableColumn[];
  /**
   * The rows of the table.
   */
  rows: Record<string, unknown>[];
  /**
   * The field on each row that is unique.
   */
  rowKey: string | ((row: Record<string, unknown>) => string);
  /**
   * The name of an item.
   */
  itemName?: string;
  /**
   * Whether to display loading state.
   */
  loading?: boolean;
  /**
   * The default row key to group by.
   */
  defaultGroupBy?: string;
  /**
   * The default row keys to sort by.
   */
  defaultSortBy?: string;
  /**
   * Determines whether a row should be visible.
   */
  filterRow?(row: Record<string, unknown>): boolean;
  /**
   * Whether table rows can be expanded.
   */
  expandable?: boolean;
  /**
   * The ids of expanded rows.
   */
  expanded?: string[];
  /**
   * Any cells can be customized through the slot `body-cell-[name]`.
   */
  customCells?: string[];
}>();

defineEmits<{
  (e: "update:expanded", expanded: string[]): void;
}>();

const { searchText, searchLabel, filteredRows } = useTableFilter(props);

const groupBy = ref<string | undefined>(props.defaultGroupBy);
const sortBy = ref<string | undefined>(props.defaultSortBy);
const sortDesc = ref(false);

const expandedRows = useVModel(props, "expanded");

const customCellSlots = computed(() =>
  props.customCells ? props.customCells.map((name) => `body-cell-${name}`) : []
);
</script>
