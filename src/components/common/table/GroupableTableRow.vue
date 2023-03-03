<template>
  <q-tr v-if="groupBy">
    <q-td colspan="100%" class="bg-background">
      <div>
        <flex-box align="center" justify="between">
          <flex-box align="center">
            <typography
              :value="groupHeader"
              r="2"
              data-cy="artifact-table-group-type"
            />
            <attribute-chip
              :value="groupValue"
              :artifact-type="groupIsArtifactType"
              :confidence-score="groupIsScore"
              data-cy="artifact-table-group-value"
            />
            <attribute-chip
              v-if="groupDisplayArtifact"
              :value="groupHeaderType"
              artifact-type
            />
            <typography secondary :value="groupRows" x="2" />
          </flex-box>
          <flex-box>
            <icon-button
              small
              color="negative"
              tooltip="Collapse All"
              icon="group-close-all"
              @click="emit('group:close', groupBy, props.row.$groupValue)"
            />
            <icon-button
              small
              color="primary"
              tooltip="Expand All"
              icon="group-open-all"
              @click="emit('group:open', groupBy, props.row.$groupValue)"
            />
          </flex-box>
        </flex-box>
        <typography
          default-expanded
          variant="expandable"
          :value="groupHeaderDescription"
        />
      </div>
    </q-td>
  </q-tr>
  <q-tr
    v-else
    :props="props.quasarProps"
    class="cursor-pointer"
    @click="handleExpand"
  >
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
  <q-tr v-if="!groupBy" v-show="props.expand" :props="props.quasarProps">
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
import { computed, useSlots } from "vue";
import { TableColumn, TableGroupRow } from "@/types";
import { camelcaseToDisplay } from "@/util";
import { artifactStore, useVModel } from "@/hooks";
import { Typography, AttributeChip } from "@/components/common/display";
import { IconButton } from "@/components/common/button";
import { FlexBox } from "@/components/common/layout";

const props = defineProps<{
  /**
   * Props passed in from the quasar table.
   */
  quasarProps: Record<string, unknown>;
  /**
   A generic row of a table, or a group header.
   */
  row: TableGroupRow;
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

const emit = defineEmits<{
  (e: "update:expanded", expanded: boolean): void;
  (e: "group:open", groupBy: string, groupValue: unknown): void;
  (e: "group:close", groupBy: string, groupValue: unknown): void;
}>();

const slots = useSlots();

const rowExpanded = useVModel(props, "expand");

const groupBy = computed(() => String(props.row.$groupBy || ""));
const groupHeader = computed(() => `${camelcaseToDisplay(groupBy.value)}:`);
const groupValue = computed(() => String(props.row.$groupValue));
const groupRows = computed(() => String(props.row.$groupRows));

const groupIsArtifactType = computed(() =>
  ["sourceType", "targetType", "type"].includes(groupBy.value)
);
const groupIsScore = computed(() => groupBy.value === "score");
const groupDisplayArtifact = computed(() =>
  ["sourceName", "targetName"].includes(groupBy.value)
);
const groupHeaderType = computed(() =>
  groupDisplayArtifact.value
    ? artifactStore.getArtifactByName(groupValue.value)?.type
    : undefined
);
const groupHeaderDescription = computed(() =>
  groupDisplayArtifact.value
    ? artifactStore.getArtifactByName(groupValue.value)?.body
    : undefined
);

/**
 * Expands the row.
 */
function handleExpand(): void {
  rowExpanded.value = !rowExpanded.value;
}
</script>
