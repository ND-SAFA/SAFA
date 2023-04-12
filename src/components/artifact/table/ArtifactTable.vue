<template>
  <panel-card>
    <groupable-table
      v-model:group-by="groupBy"
      :columns="columns"
      :rows="rows"
      row-key="id"
      default-sort-by="name"
      :default-group-by="groupBy"
      :loading="loading"
      :filter-row="filterRow"
      :custom-cells="customCells"
      data-cy="view-artifact-table"
      @row-click="handleView"
    >
      <template #header-right>
        <multiselect-input
          v-if="inDeltaView"
          v-model="deltaTypes"
          outlined
          dense
          :use-chips="false"
          :options="options"
          label="Delta Types"
          option-to-value
          option-value="id"
          option-label="name"
          class="table-input"
          data-cy="input-delta-type"
          b=""
        />
      </template>

      <template #body-cell-type="{ row }">
        <attribute-chip :value="row.type" artifact-type />
      </template>

      <template #body-cell-deltaType="{ row }">
        <attribute-chip :value="getDeltaType(row)" delta-type />
      </template>

      <template #body-cell-actions="{ row }">
        <div @click.stop>
          <artifact-table-row-actions :artifact="row" />
        </div>
      </template>
    </groupable-table>
  </panel-card>
</template>

<script lang="ts">
/**
 Represents a table of artifacts.
 */
export default {
  name: "ArtifactTable",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { ArtifactDeltaState, FlatArtifact, TableGroupRow } from "@/types";
import {
  deltaTypeOptions,
  artifactAttributesColumns,
  artifactColumns,
  artifactDeltaColumn,
  actionsColumn,
} from "@/util";
import {
  appStore,
  artifactStore,
  attributesStore,
  deltaStore,
  selectionStore,
} from "@/hooks";
import {
  PanelCard,
  GroupableTable,
  AttributeChip,
  MultiselectInput,
} from "@/components/common";
import ArtifactTableRowActions from "./ArtifactTableRowActions.vue";

const customCells: (keyof FlatArtifact | string)[] = [
  "type",
  "deltaType",
  "actions",
];

const options = deltaTypeOptions();

const groupBy = ref<string | undefined>("type");
const deltaTypes = ref<ArtifactDeltaState[]>([]);

const loading = computed(() => appStore.isLoading > 0);
const inDeltaView = computed(() => deltaStore.inDeltaView);

const columns = computed(() => [
  ...artifactColumns,
  ...(inDeltaView.value ? [artifactDeltaColumn] : []),
  ...artifactAttributesColumns(attributesStore.attributes),
  actionsColumn,
]);

const rows = computed(() => artifactStore.flatArtifacts);

/**
 * Filters out rows that don't match the selected delta types.
 * @param row - The artifact to filter.
 * @return Whether to keep the row.
 */
function filterRow(row: FlatArtifact): boolean {
  return (
    !inDeltaView.value ||
    deltaTypes.value.length === 0 ||
    deltaTypes.value.includes(getDeltaType(row))
  );
}

/**
 * Returns the delta type for a row.
 * @param row - The artifact to check.
 * @return The type of change delta loaded for this artifact.
 */
function getDeltaType(row: FlatArtifact): ArtifactDeltaState {
  return deltaStore.getArtifactDeltaType(row.id);
}

/**
 * Opens the view artifact side panel.
 * @param row - The artifact to view.
 */
function handleView(row: TableGroupRow | FlatArtifact) {
  if ("id" in row) {
    selectionStore.toggleSelectArtifact(String(row.id));
  }
}
</script>
