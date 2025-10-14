<template>
  <panel-card>
    <groupable-table
      v-model:group-by="groupBy"
      :columns="columns"
      :rows="rows"
      row-key="id"
      default-sort-by="name"
      :loading="loading"
      :filter-row="filterRow"
      :custom-cells="customCells"
      data-cy="view-trace-matrix-table"
      @row-click="handleView"
    >
      <template #header-right>
        <multiselect-input
          v-model="rowTypes"
          outlined
          dense
          clearable
          :use-chips="false"
          :options="options"
          label="Row Types"
          b=""
          class="q-mr-sm q-mb-sm table-input"
          data-cy="input-trace-table-row-types"
        />
        <multiselect-input
          v-model="colTypes"
          outlined
          dense
          clearable
          :use-chips="false"
          :options="options"
          label="Column Types"
          b=""
          class="table-input q-mb-sm"
          data-cy="input-trace-table-col-types"
        />
      </template>

      <template #body-cell-type="{ row }: { row: ArtifactSchema }">
        <attribute-chip :value="row.type" artifact-type />
      </template>

      <template
        v-for="artifact in columnArtifacts"
        #[`body-cell-${artifact.id}`]="{ row }"
        :key="artifact.id"
      >
        <trace-matrix-chip :source="row" :target="artifact" />
      </template>
    </groupable-table>
  </panel-card>
</template>

<script lang="ts">
/**
 Displays a matrix of artifacts and their relationships.
 */
export default {
  name: "TraceTable",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { ArtifactSchema, FlatArtifact, TableGroupRow } from "@/types";
import { artifactColumns, artifactMatrixColumns } from "@/util";
import { appStore, artifactStore, selectionStore, timStore } from "@/hooks";
import {
  PanelCard,
  GroupableTable,
  AttributeChip,
  MultiselectInput,
} from "@/components/common";
import TraceMatrixChip from "./TraceMatrixChip.vue";

const groupBy = ref<string | undefined>("type");
const rowTypes = ref<string[]>([]);
const colTypes = ref<string[]>([]);

const loading = computed(() => appStore.isLoading > 0);

const options = computed(() => timStore.typeNames);

const rows = computed(() => artifactStore.currentArtifacts);

const columnArtifacts = computed(() =>
  artifactStore.currentArtifacts.filter(
    ({ type }) => colTypes.value.length === 0 || colTypes.value.includes(type)
  )
);

const columns = computed(() => [
  ...artifactColumns,
  ...artifactMatrixColumns(columnArtifacts.value),
]);

const customCells = computed(() => [
  "type",
  ...columnArtifacts.value.map(({ id }) => id),
]);

/**
 * Filters out rows that don't match the selected row types.
 * @param row - The artifact to filter.
 * @return Whether to keep the row.
 */
function filterRow(row: FlatArtifact): boolean {
  return rowTypes.value.length === 0 || rowTypes.value.includes(row.type);
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
