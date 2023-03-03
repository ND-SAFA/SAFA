<template>
  <q-tr :props="props.quasarProps" class="cursor-pointer" @click="handleExpand">
    <q-td
      v-for="(column, idx) in props.columns"
      :key="column.name"
      :align="idx === 0 ? 'start' : 'end'"
    >
      <icon-button
        v-if="idx === 0 && props.expandable"
        tooltip="Toggle expand"
        :icon="props.expand ? 'up' : 'down'"
        class="q-mr-sm"
      />
      <slot
        v-if="!!slots[`body-cell-${column.name}`]"
        :name="`body-cell-${column.name}`"
        :row="props.row"
      />
      <typography v-else :value="String(column.field(props.row))" />
    </q-td>
  </q-tr>
  <q-tr v-show="props.expand" :props="props.quasarProps">
    <q-td colspan="100%">
      <slot name="body-expanded" :row="props.row" />
    </q-td>
  </q-tr>
</template>

<script lang="ts">
/**
 * Renders a row of the groupable table.
 */
export default {
  name: "GroupableTableRow",
};
</script>

<script setup lang="ts">
import { useSlots } from "vue";
import { TableColumn } from "@/types";
import { useVModel } from "@/hooks";
import { Typography } from "@/components/common/display";
import IconButton from "@/components/common/button/IconButton.vue";

const props = defineProps<{
  /**
   * Props passed in from the quasar table.
   */
  quasarProps: Record<string, unknown>;
  /**
   * The row to render.
   */
  row: Record<string, unknown>;
  /**
   * The visible table columns.
   */
  columns: TableColumn[];
  /**
   * Whether the row can be expanded.
   */
  expandable?: boolean;
  /**
   * Whether the row is expanded.
   */
  expand?: boolean;
}>();

defineEmits<{
  (e: "update:expanded", expanded: boolean): void;
}>();

const slots = useSlots();

const rowExpanded = useVModel(props, "expand");

/**
 * Expands the row.
 */
function handleExpand(): void {
  rowExpanded.value = !rowExpanded.value;
}
</script>
