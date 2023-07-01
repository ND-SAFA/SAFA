<template>
  <data-table
    v-model:sort-by="sortBy"
    v-model:sort-desc="sortDesc"
    v-model:expanded="expandedRows"
    virtual-scroll
    :columns="props.columns"
    :rows="groupedRows"
    :row-key="props.rowKey"
    :loading="props.loading"
    :expanded="props.expandable ? expandedRows : undefined"
    :sort="(r) => r"
    separator="cell"
  >
    <template #top="scope">
      <groupable-table-header
        v-model:search-text="searchText"
        v-model:group-by="groupBy"
        v-model:sort-by="sortBy"
        v-model:sort-desc="sortDesc"
        :columns="columns"
        :search-label="searchLabel"
        :in-fullscreen="scope.inFullscreen"
        @toggle-fullscreen="scope.toggleFullscreen"
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
        @click="emit('row-click', quasarProps.row)"
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
import { GroupableTableProps, TableGroupRow, TableRow } from "@/types";
import { useTableFilter, useVModel } from "@/hooks";
import GroupableTableRow from "./GroupableTableRow.vue";
import GroupableTableHeader from "./GroupableTableHeader.vue";
import DataTable from "./DataTable.vue";

const props = defineProps<GroupableTableProps>();

const emit = defineEmits<{
  (e: "update:expanded", expanded: string[]): void;
  (e: "update:groupBy", groupBy: string | undefined): void;
  (e: "group:open", groupBy: string, groupValue: unknown): void;
  (e: "group:close", groupBy: string, groupValue: unknown): void;
  (e: "row-click", row: TableRow): void;
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
        id: `${groupBy.value}::${$groupValue}`,
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
