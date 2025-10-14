<template>
  <private-page full-window graph class="bg-neutral">
    <project-tree />

    <project-chat />

    <div
      v-if="isTableMode"
      class="q-pa-sm bg-background"
      style="min-height: inherit"
    >
      <tab-list v-model="tab" :tabs="tabs">
        <template #artifact>
          <artifact-table />
        </template>
        <template #trace>
          <approval-table />
        </template>
        <template #matrix>
          <trace-table />
        </template>
      </tab-list>
    </div>
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
  TabList,
  TraceTable,
  ProjectTree,
  ApprovalTable,
  ProjectChat,
} from "@/components";

const tabs = tableViewTabOptions();

const tab = ref(tabs[0].id);

const isTableMode = computed(() => layoutStore.isTableMode);
</script>
