<template>
  <private-page full-window graph class="bg-neutral">
    <project-tree />
    <graph-fab />

    <tab-list
      v-if="isTableMode"
      v-model="tab"
      :tabs="tabs"
      class="q-pa-lg bg-background"
      style="min-height: inherit"
    >
      <template #artifact>
        <artifact-table />
      </template>
      <template #trace>
        <trace-table />
      </template>
      <template #approve>
        <approval-table />
      </template>
    </tab-list>
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the artifact tree and table.
 */
export default {
  name: "ArtifactView",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { tableViewTabOptions } from "@/util";
import { layoutStore, permissionStore } from "@/hooks";
import {
  ArtifactTable,
  PrivatePage,
  GraphFab,
  TabList,
  TraceTable,
  ProjectTree,
  ApprovalTable,
} from "@/components";

const displayEditing = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);

const tabs = computed(() =>
  displayEditing.value ? tableViewTabOptions() : [tableViewTabOptions()[0]]
);
const tab = ref(tabs.value[0].id);

const isTableMode = computed(() => layoutStore.isTableMode);
</script>
