<template>
  <div class="full-width">
    <flex-box full-width align="center">
      <searchbar v-model="searchText" :label="props.searchLabel" />
      <commit-buttons color="primary" class="q-ml-md" />
    </flex-box>
    <flex-box align="center" t="2">
      <select-input
        v-model="groupBy"
        outlined
        clearable
        dense
        label="Group By"
        :options="inputOptions"
        option-value="name"
        option-label="label"
        option-to-value
        data-cy="artifact-table-group-by"
      />
      <select-input
        v-model="sortBy"
        outlined
        clearable
        dense
        label="Sort By"
        :options="inputOptions"
        option-value="name"
        option-label="label"
        option-to-value
        class="q-ml-sm"
        data-cy="artifact-table-sort-by"
      >
        <template #prepend>
          <div @click.stop="">
            <icon-button
              small
              tooltip="Toggle sort direction"
              :icon="sortDesc ? 'arrow-down' : 'arrow-up'"
              @click="sortDesc = !sortDesc"
            />
          </div>
        </template>
      </select-input>
      <separator v-if="!!slots['header-right']" vertical class="q-mx-sm" />
      <slot name="header-right" />
    </flex-box>
    <slot name="header-bottom" />
  </div>
</template>

<script lang="ts">
/**
 * header inputs for a table that can be grouped and expanded.
 */
export default {
  name: "GroupableTableHeader",
};
</script>

<script setup lang="ts">
import { computed, useSlots } from "vue";
import { TableColumn } from "@/types";
import { useVModel } from "@/hooks";
import { Searchbar, SelectInput } from "@/components/common/input";
import { CommitButtons, IconButton } from "@/components/common/button";
import { FlexBox } from "@/components/common/layout";
import { Separator } from "@/components/common/display";

const props = defineProps<{
  /**
   * The columns to render in the table.
   */
  columns: TableColumn[];
  /**
   * The search text to filter with.
   */
  searchText: string;
  /**
   * The label for the searchbar.
   */
  searchLabel: string;
  /**
   * The row key to group by.
   */
  groupBy: string | undefined;
  /**
   * The row keys to sort by.
   */
  sortBy: string | undefined;
  /**
   * Whether to sort in descending order.
   */
  sortDesc: boolean;
}>();

defineEmits<{
  (e: "update:searchText", text: string): void;
  (e: "update:sortBy", values: string | undefined): void;
  (e: "update:sortDesc", descending: boolean): void;
  (e: "update:groupBy", value: string | undefined): void;
}>();

const searchText = useVModel(props, "searchText");
const sortBy = useVModel(props, "sortBy");
const sortDesc = useVModel(props, "sortDesc");
const groupBy = useVModel(props, "groupBy");

const slots = useSlots();

const inputOptions = computed(() =>
  props.columns
    .filter(({ name }) => name !== "actions")
    .map(({ name, label }) => ({ name, label }))
);
</script>
