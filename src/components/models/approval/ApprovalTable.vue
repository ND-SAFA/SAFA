<template>
  <panel-card>
    <groupable-table
      v-model:group-by="groupBy"
      v-model:expanded="expanded"
      expandable
      :columns="columns"
      :rows="rows"
      row-key="traceLinkId"
      :loading="loading"
      default-sort-by="score"
      :default-group-by="groupBy"
      default-sort-desc
      :filter-row="filterRow"
      :custom-cells="customCells"
      data-cy="table-trace-approval"
      @group:open="handleOpenGroup"
      @group:close="handleCloseGroup"
    >
      <template #header-right>
        <multiselect-input
          v-model="approvalTypes"
          outlined
          dense
          :use-chips="false"
          :options="options"
          label="Approval Types"
          option-to-value
          option-value="id"
          option-label="name"
          data-cy="input-approval-type"
          b=""
        />
        <text-button
          text
          small
          label="Clear Unreviewed"
          icon="trace-decline-all"
          color="negative"
          class="q-ml-sm"
          @click="handleDeclineAll"
        />
      </template>

      <template #body-cell-sourceType="{ row }">
        <attribute-chip :value="row.sourceType" artifact-type />
      </template>

      <template #body-cell-targetType="{ row }">
        <attribute-chip :value="row.targetType" artifact-type />
      </template>

      <template #body-cell-approvalStatus="{ row }">
        <attribute-chip :value="row.approvalStatus" approval-type />
      </template>

      <template #body-cell-score="{ row }">
        <attribute-chip :value="row.score" confidence-score />
      </template>

      <template #body-cell-actions="{ row }">
        <trace-link-approval v-if="displayActions" :trace="row" />
      </template>

      <template #body-expanded="{ row }">
        <trace-link-display :trace="row" :show-only="expandedDisplay" />
      </template>
    </groupable-table>
  </panel-card>
</template>

<script lang="ts">
/**
 Displays a table of generated trace links for approval.
 */
export default {
  name: "ApprovalTable",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { ApprovalType, FlatTraceLink } from "@/types";
import { approvalTypeOptions, approvalColumns } from "@/util";
import { approvalStore, appStore, projectStore, sessionStore } from "@/hooks";
import { Routes } from "@/router";
import { handleDeclineAll, handleGetGeneratedLinks } from "@/api";
import {
  PanelCard,
  GroupableTable,
  MultiselectInput,
  TextButton,
  AttributeChip,
} from "@/components/common";
import { TraceLinkApproval, TraceLinkDisplay } from "@/components/traceLink";

const options = approvalTypeOptions();

const customCells: (keyof FlatTraceLink | string)[] = [
  "sourceType",
  "targetType",
  "approvalStatus",
  "score",
  "actions",
];

const currentRoute = useRoute();

const approvalTypes = ref<ApprovalType[]>([ApprovalType.UNREVIEWED]);
const groupBy = ref<string | undefined>("targetName");

const displayActions = computed(() =>
  sessionStore.isEditor(projectStore.project)
);

const rows = computed(() => approvalStore.traceLinks);

const loading = computed(() => appStore.isLoading > 0);

const expanded = computed({
  get() {
    return approvalStore.expandedIds;
  },
  set(ids) {
    approvalStore.expandedIds = ids;
  },
});

/**
 * @return What parts of the expansion panel to show.
 */
const expandedDisplay = computed<undefined | "source" | "target">(() => {
  switch (groupBy.value) {
    case "sourceName":
      return "target";
    case "targetName":
      return "source";
    default:
      return undefined;
  }
});

const columns = computed(() =>
  approvalColumns.filter(
    (col) =>
      !(
        (approvalTypes.value.length === 1 && col.name === "approvalStatus") ||
        (groupBy.value === "sourceName" && col.name === "sourceType") ||
        (groupBy.value === "targetName" && col.name === "targetType")
      )
  )
);

/**
 * Refreshes table data.
 */
function handleRefresh() {
  handleGetGeneratedLinks({});
}

/**
 * Filters out rows that don't match the selected approval types.
 * @param row - The row to filter.
 * @return Whether to keep the row.
 */
function filterRow(row: FlatTraceLink): boolean {
  return (
    approvalTypes.value.length === 0 ||
    approvalTypes.value.includes(row.approvalStatus)
  );
}

onMounted(() => handleRefresh());

watch(
  () => currentRoute.path,
  (path) => {
    if (path !== Routes.TRACE_LINK) return;

    handleRefresh();
  }
);

watch(
  () => projectStore.versionId,
  (versionId) => {
    if (!versionId) return;

    handleRefresh();
  }
);

/**
 * Expands all panels in the group.
 * @param groupBy - The grouped field.
 * @param groupValue - The grouped value.
 */
function handleOpenGroup(groupBy: keyof FlatTraceLink, groupValue: unknown) {
  approvalStore.expandLinks((link) => link[groupBy] === groupValue);
}

/**
 * Collapses all panels in the group.
 * @param groupBy - The grouped field.
 * @param groupValue - The grouped value.
 */
function handleCloseGroup(groupBy: keyof FlatTraceLink, groupValue: unknown) {
  approvalStore.collapseLinks((link) => link[groupBy] !== groupValue);
}
</script>
