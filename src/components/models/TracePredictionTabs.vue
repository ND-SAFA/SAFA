<template>
  <sidebar-grid>
    <template v-slot:header>
      <trace-prediction-header />
    </template>
    <template v-slot:sidebar>
      <project-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <v-tab-item key="1">
        <model-table />
      </v-tab-item>
      <v-tab-item key="2">
        <v-container style="max-width: 50em">
          <v-card outlined class="pa-2">
            <trace-link-generator :is-open="tab === 1" />
          </v-card>
        </v-container>
      </v-tab-item>
      <v-tab-item key="3">
        <trace-link-table />
      </v-tab-item>
    </tab-list>
  </sidebar-grid>
</template>

<script lang="ts">
import Vue from "vue";
import { tracePredictionTabOptions } from "@/util";
import { TabList, SidebarGrid } from "@/components/common";
import { TraceLinkTable, TraceLinkGenerator } from "@/components/traceLink";
import { ProjectDisplay } from "@/components/project";
import { ModelTable } from "./table";
import TracePredictionHeader from "./TracePredictionHeader.vue";

/**
 * Tabs for predicting and approving trace links.
 */
export default Vue.extend({
  name: "TracePredictionTabs",
  components: {
    SidebarGrid,
    TracePredictionHeader,
    ProjectDisplay,
    TraceLinkGenerator,
    ModelTable,
    TraceLinkTable,
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
