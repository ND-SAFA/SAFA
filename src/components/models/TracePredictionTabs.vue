<template>
  <sidebar-grid>
    <template #header>
      <trace-prediction-header />
    </template>
    <template #sidebar>
      <project-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <v-window-item key="1">
        <model-table />
      </v-window-item>
      <v-window-item key="2">
        <panel-card>
          <trace-link-generator :is-open="tab === 1" />
        </panel-card>
      </v-window-item>
      <v-window-item key="3">
        <trace-approval-table />
      </v-window-item>
    </tab-list>
  </sidebar-grid>
</template>

<script lang="ts">
import Vue from "vue";
import { tracePredictionTabOptions } from "@/util";
import { TabList, SidebarGrid, PanelCard } from "@/components/common";
import { TraceLinkGenerator } from "@/components/traceLink";
import { ProjectDisplay } from "@/components/project";
import { ModelTable } from "./training";
import { TraceApprovalTable } from "./approval";
import TracePredictionHeader from "./TracePredictionHeader.vue";

/**
 * Tabs for predicting and approving trace links.
 */
export default Vue.extend({
  name: "TracePredictionTabs",
  components: {
    PanelCard,
    SidebarGrid,
    TracePredictionHeader,
    ProjectDisplay,
    TraceLinkGenerator,
    ModelTable,
    TraceApprovalTable,
    TabList,
  },
  data() {
    return {
      tab: 0,
      tabs: tracePredictionTabOptions(),
    };
  },
});
</script>
