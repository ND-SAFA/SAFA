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
          v-model="visibleTypes"
          outlined
          dense
          clearable
          :use-chips="false"
          :options="typeOptions"
          label="Visible Types"
          b=""
          class="q-mr-sm table-input"
          data-cy="input-trace-table-types"
        />
        <select-input
          v-model="countType"
          outlined
          dense
          :options="countOptions"
          option-to-value
          option-label="name"
          option-value="id"
          label="Visible Types"
          b=""
          class="q-mr-sm table-input"
          data-cy="input-trace-table-count"
        />
        <multiselect-input
          v-if="inDeltaView"
          v-model="deltaTypes"
          outlined
          dense
          :use-chips="false"
          :options="deltaOptions"
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
import {
  ArtifactDeltaState,
  FlatArtifact,
  TableGroupRow,
  TraceCountTypes,
} from "@/types";
import {
  deltaTypeOptions,
  artifactAttributesColumns,
  artifactColumns,
  artifactDeltaColumn,
  actionsColumn,
  traceCountOptions,
} from "@/util";
import {
  appStore,
  artifactStore,
  attributesStore,
  deltaStore,
  selectionStore,
  subtreeStore,
  typeOptionsStore,
} from "@/hooks";
import {
  PanelCard,
  GroupableTable,
  AttributeChip,
  MultiselectInput,
} from "@/components/common";
import SelectInput from "@/components/common/input/SelectInput.vue";
import ArtifactTableRowActions from "./ArtifactTableRowActions.vue";

const customCells: (keyof FlatArtifact | string)[] = [
  "type",
  "deltaType",
  "actions",
];

const deltaOptions = deltaTypeOptions();
const countOptions = traceCountOptions();

const groupBy = ref<string | undefined>("type");
const visibleTypes = ref<string[]>([]);
const countType = ref<TraceCountTypes>(TraceCountTypes.all);
const deltaTypes = ref<ArtifactDeltaState[]>([]);

const loading = computed(() => appStore.isLoading > 0);
const inDeltaView = computed(() => deltaStore.inDeltaView);
const typeOptions = computed(() => typeOptionsStore.artifactTypes);

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
  const subtree = subtreeStore.getSubtreeItem(row.id);

  return (
    (visibleTypes.value.length === 0 ||
      visibleTypes.value.includes(row.type)) &&
    (!inDeltaView.value ||
      deltaTypes.value.length === 0 ||
      deltaTypes.value.includes(getDeltaType(row))) &&
    (countType.value === TraceCountTypes.all ||
      (countType.value === TraceCountTypes.onlyTraced &&
        subtree.neighbors.length > 0) ||
      (countType.value === TraceCountTypes.notTraced &&
        subtree.neighbors.length === 0))
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
