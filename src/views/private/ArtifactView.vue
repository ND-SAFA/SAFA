<template>
  <private-page full-window>
    <project-tree />
    <artifact-fab />

    <tab-list
      v-if="layoutStore.isTableMode"
      v-model="tab"
      :tabs="tabs"
      class="my-4 mx-10"
    >
      <v-window-item key="1">
        <artifact-table />
      </v-window-item>
      <v-window-item key="2">
        <trace-matrix-table />
      </v-window-item>
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
import { ref } from "vue";
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
const tab = ref(0);
</script>
