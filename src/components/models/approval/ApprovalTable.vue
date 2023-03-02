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
    >
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
import { computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { approvalStore, appStore, projectStore } from "@/hooks";
import { Routes } from "@/router";
import { handleGetGeneratedLinks } from "@/api";
import { PanelCard, GroupableTable } from "@/components/common";
import { approvalColumns } from "./headers";

const currentRoute = useRoute();

const rows = computed(() => approvalStore.traceLinks);

const loading = computed(() => appStore.isLoading > 0);

/**
 * Refreshes table data.
 */
function handleRefresh() {
  handleGetGeneratedLinks({});
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
