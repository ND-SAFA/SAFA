<template>
  <private-page full-window graph>
    <project-tree />
    <artifact-fab />

    <tab-list v-if="isTableMode" v-model="tab" :tabs="tabs" class="q-ma-lg">
      <template #artifacts>
        <artifact-table />
      </template>
      <template #traces>
        <trace-matrix-table />
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
  TraceMatrixTable,
  ProjectTree,
} from "@/components";

const tabs = tableViewTabOptions();
const tab = ref("artifacts");

const isTableMode = computed(() => layoutStore.isTableMode);
</script>
