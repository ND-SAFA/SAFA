<template>
  <panel-card>
    <groupable-table
      v-model:group-by="groupBy"
      v-model:expanded="expanded"
      expandable
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
      @group:open="handleOpenGroup"
      @group:close="handleCloseGroup"
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
          class="table-input q-mb-sm q-mr-sm"
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
          label="Visible Artifacts"
          b=""
          class="table-input q-mb-sm q-mr-sm"
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
          class="table-input q-mb-sm q-mr-sm"
          data-cy="input-delta-type"
          b=""
        />
        <q-btn-group
          v-if="!documentStore.isBaseDocument"
          flat
          class="q-mb-sm nav-mode-select"
        >
          <text-button
            label="Current View"
            v-bind="buttonProps('view')"
            @click="showAll = false"
          />
          <text-button
            label="All Artifacts"
            v-bind="buttonProps('all')"
            @click="showAll = true"
          />
        </q-btn-group>
      </template>

      <template #body-expanded="{ row }">
        <artifact-content-display :artifact="row" />
      </template>

      <template #body-cell-name="{ row }">
        <artifact-name-display :artifact="row" display-tooltip />
      </template>

      <template #body-cell-type="{ row }: { row: FlatArtifact }">
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
  documentStore,
  selectionStore,
  subtreeStore,
  timStore,
} from "@/hooks";
import {
  PanelCard,
  GroupableTable,
  AttributeChip,
  MultiselectInput,
  SelectInput,
} from "@/components/common";
import {
  ArtifactContentDisplay,
  ArtifactNameDisplay,
} from "@/components/artifact/display";
import TextButton from "@/components/common/button/TextButton.vue";
import ArtifactTableRowActions from "./ArtifactTableRowActions.vue";

const customCells: (keyof FlatArtifact | string)[] = [
  "name",
  "type",
  "deltaType",
  "actions",
];

const deltaOptions = deltaTypeOptions();
const countOptions = traceCountOptions();

const groupBy = ref<string | undefined>("type");
const visibleTypes = ref<string[] | null>([]);
const countType = ref<TraceCountTypes>("all");
const deltaTypes = ref<ArtifactDeltaState[] | null>([]);

const loading = computed(() => appStore.isLoading > 0);
const inDeltaView = computed(() => deltaStore.inDeltaView);
const typeOptions = computed(() => timStore.typeNames);

const expanded = ref<string[]>([]);
const showAll = ref(false);

const columns = computed(() => [
  ...artifactColumns,
  ...(inDeltaView.value ? [artifactDeltaColumn] : []),
  ...artifactAttributesColumns(attributesStore.attributes),
  actionsColumn,
]);

const rows = computed(() => artifactStore.getFlatArtifacts(showAll.value));

/**
 * Returns props for a mode button.
 * @param mode - The mode button to get props for.
 */
function buttonProps(mode: "all" | "view") {
  const selected = mode === "all" ? showAll.value : !showAll.value;

  return {
    text: !selected,
    outlined: selected,
    color: "text",
  };
}

/**
 * Filters out rows that don't match the selected delta types.
 * @param row - The artifact to filter.
 * @return Whether to keep the row.
 */
function filterRow(row: FlatArtifact): boolean {
  const subtree = subtreeStore.getSubtreeItem(row.id);
  const visible = visibleTypes.value || [];
  const delta = deltaTypes.value || [];

  return (
    ((visible.length || 0) === 0 || visible.includes(row.type)) &&
    (!inDeltaView.value ||
      delta.length === 0 ||
      delta.includes(getDeltaType(row))) &&
    (countType.value === "all" ||
      (countType.value === "onlyTraced" && subtree.neighbors.length > 0) ||
      (countType.value === "notTraced" && subtree.neighbors.length === 0))
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

/**
 * Expands all panels in the group.
 * @param groupBy - The grouped field.
 * @param groupValue - The grouped value.
 */
function handleOpenGroup(groupBy: keyof FlatArtifact, groupValue: unknown) {
  expanded.value = rows.value
    .filter((row) => row[groupBy] === groupValue)
    .map((row) => row.id);
}

/**
 * Collapses all panels in the group.
 * @param groupBy - The grouped field.
 * @param groupValue - The grouped value.
 */
function handleCloseGroup(groupBy: keyof FlatArtifact, groupValue: unknown) {
  expanded.value = rows.value
    .filter(
      (row) => expanded.value.includes(row.id) && row[groupBy] !== groupValue
    )
    .map((row) => row.id);
}
</script>
