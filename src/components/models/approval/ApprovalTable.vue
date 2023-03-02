<template>
  <panel-card
    title="Approve Generated Links"
    subtitle="Review, approve, and decline generated trace links."
  >
    <groupable-table
      :columns="approvalColumns"
      :rows="rows"
      row-key="traceLinkId"
      :loading="loading"
      default-sort-by="sourceName"
      :filter-row="filterRow"
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
        />
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
import { approvalTypeOptions } from "@/util";
import { approvalStore, appStore, projectStore } from "@/hooks";
import { Routes } from "@/router";
import { handleGetGeneratedLinks } from "@/api";
import {
  PanelCard,
  GroupableTable,
  MultiselectInput,
} from "@/components/common";
import { approvalColumns } from "./headers";

const options = approvalTypeOptions();

const currentRoute = useRoute();

const approvalTypes = ref<ApprovalType[]>([ApprovalType.UNREVIEWED]);

const rows = computed(() => approvalStore.traceLinks);

const loading = computed(() => appStore.isLoading > 0);

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
</script>
