<template>
  <private-page full-window>
    <template v-slot:page>
      <project-tree />
      <artifact-fab />

      <tab-list
        v-if="isTableView"
        v-model="tab"
        :tabs="tabs"
        class="my-4 mx-10"
      >
        <v-tab-item key="1">
          <artifact-table />
        </v-tab-item>
        <v-tab-item key="2">
          <trace-matrix-table />
        </v-tab-item>
      </tab-list>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
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

/**
 * Displays the artifact tree and table.
 */
export default Vue.extend({
  name: "ArtifactView",
  components: {
    ProjectTree,
    TraceMatrixTable,
    TabList,
    ArtifactFab,
    ArtifactTable,
    PrivatePage,
  },
  data() {
    return {
      tab: 0,
      tabs: tableViewTabOptions(),
    };
  },
  computed: {
    /**
     * @return Whether table view is enabled.
     */
    isTableView(): boolean {
      return layoutStore.isTableMode;
    },
  },
});
</script>
