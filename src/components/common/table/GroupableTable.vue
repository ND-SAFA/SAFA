<template>
  <data-table
    v-model:sort-by="sortBy"
    v-model:sort-desc="sortDesc"
    :columns="props.columns"
    :rows="filteredRows"
    :row-key="props.rowKey"
    :loading="props.loading"
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
import { ref } from "vue";
import { TableColumn } from "@/types";
import { useTableFilter } from "@/hooks";
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
}>();

// const emit = defineEmits<{}>();

const { searchText, searchLabel, filteredRows } = useTableFilter(props);

const groupBy = ref<string | undefined>(props.defaultGroupBy);
const sortBy = ref<string | undefined>(props.defaultSortBy);
const sortDesc = ref(false);
</script>
