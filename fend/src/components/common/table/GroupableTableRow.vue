<template>
  <q-tr v-if="groupBy" data-cy="artifact-table-group">
    <q-td colspan="100%">
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
              v-if="groupDisplayArtifact && groupHeaderType"
              :value="groupHeaderType"
              artifact-type
            />
            <typography secondary :value="groupRows" x="2" />
          </flex-box>
          <flex-box v-if="props.expandable">
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
          v-if="!!groupHeaderDescription"
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
    @click="emit('click')"
  >
    <q-td v-for="(column, idx) in props.columns" :key="column.name">
      <flex-box align="center" :justify="idx === 0 ? 'start' : 'end'">
        <div @click.stop>
          <icon-button
            v-if="idx === 0 && props.expandable"
            tooltip="Toggle expand"
            :icon="props.expand ? 'up' : 'down'"
            class="q-mr-sm"
            @click="rowExpanded = !rowExpanded"
          />
        </div>
        <slot
          v-if="!!slots[`body-cell-${column.name}`]"
          :name="`body-cell-${column.name}`"
          :row="props.row"
        />
        <typography v-else :value="getColumnDisplayValue(column)" />
      </flex-box>
    </q-td>
  </q-tr>
  <q-tr v-if="!groupBy" v-show="props.expand" :props="props.quasarProps">
    <q-td colspan="100%" class="bg-background">
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
import { GroupableTableRowProps, TableColumn } from "@/types";
import { camelcaseToDisplay } from "@/util";
import { artifactStore, useVModel } from "@/hooks";
import {
  Typography,
  AttributeChip,
  FlexBox,
} from "@/components/common/display";
import { IconButton } from "@/components/common/button";

const props = defineProps<GroupableTableRowProps>();

const emit = defineEmits<{
  (e: "click"): void;
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
 * Returns the display value for a column on this row.
 * @param column - The column to display.
 * @return The display value.
 */
function getColumnDisplayValue(column: TableColumn): string {
  return column.format
    ? column.format(column.field(props.row))
    : String(column.field(props.row));
}
</script>
