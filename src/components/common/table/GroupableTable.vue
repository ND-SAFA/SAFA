<template>
  <data-table
    v-model:sort-by="sortBy"
    v-model:sort-desc="sortDesc"
    v-model:expanded="expandedRows"
    :columns="props.columns"
    :rows="groupedRows"
    :row-key="props.rowKey"
    :loading="props.loading"
    :expanded="props.expandable ? expandedRows : undefined"
    :sort="(r) => r"
    separator="cell"
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
        @group:open="(by, val) => emit('group:open', by, val)"
        @group:close="(by, val) => emit('group:close', by, val)"
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
import { computed, ref, watch } from "vue";
import { TableColumn, TableGroupRow, TableRow } from "@/types";
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
  rows: TableRow[];
  /**
   * The field on each row that is unique.
   */
  rowKey: string | ((row: TableRow) => string);
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
   * The default sort direction.
   */
  defaultSortDesc?: boolean;
  /**
   * Determines whether a row should be visible.
   */
  filterRow?(row: TableRow): boolean;
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

const emit = defineEmits<{
  (e: "update:expanded", expanded: string[]): void;
  (e: "update:groupBy", groupBy: string | undefined): void;
  (e: "group:open", groupBy: string, groupValue: unknown): void;
  (e: "group:close", groupBy: string, groupValue: unknown): void;
}>();

const { searchText, searchLabel, sortBy, sortDesc, filteredRows } =
  useTableFilter(props);

const groupBy = ref<string | undefined>(props.defaultGroupBy);

const expandedRows = useVModel(props, "expanded");

const customCellSlots = computed(() =>
  props.customCells ? props.customCells.map((name) => `body-cell-${name}`) : []
);

/**
 * Applies sorting and grouping to filtered rows by adding header rows in between each group.
 */
const groupedRows = computed(() => {
  if (!groupBy.value) {
    return filteredRows.value;
  }

  const rowsByGroup: Record<string, TableGroupRow[]> = {};

  filteredRows.value.forEach((row) => {
    const group = String(row[groupBy.value || ""]);

    rowsByGroup[group] = [...(rowsByGroup[group] || []), row];
  });

  return Object.entries(rowsByGroup)
    .map(([$groupValue, rows]) => [
      {
        $groupValue,
        $groupBy: groupBy.value,
        $groupRows: rows.length,
      },
      ...rows,
    ])
    .reduce((acc, cur) => [...acc, ...cur], []);
});

watch(
  () => groupBy.value,
  (group) => emit("update:groupBy", group)
);
</script>
