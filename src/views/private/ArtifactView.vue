<template>
  <private-page full-window graph>
    <project-tree />
    <artifact-fab />

    <tab-list v-if="isTableMode" v-model="tab" :tabs="tabs" class="q-pa-lg">
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
import { layoutStore } from "@/hooks";
import {
  ArtifactTable,
  PrivatePage,
  ArtifactFab,
  TabList,
  TraceTable,
  ProjectTree,
  ApprovalTable,
} from "@/components";

const tabs = tableViewTabOptions();
const tab = ref(tabs[0].id);

const isTableMode = computed(() => layoutStore.isTableMode);
</script>
