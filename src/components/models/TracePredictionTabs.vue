<template>
  <v-container>
    <typography el="h1" variant="title" value="Trace Prediction" />
    <v-divider class="mb-2" />
    <project-display />
    <tab-list v-model="tab" :tabs="tabs">
      <v-tab-item key="1">
        <model-table />
      </v-tab-item>
      <v-tab-item key="2">
        <trace-link-generator :is-open="tab === 1" />
      </v-tab-item>
      <v-tab-item key="3">
        <trace-link-table />
      </v-tab-item>
    </tab-list>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { tracePredictionTabOptions } from "@/util";
import { TabList, Typography } from "@/components/common";
import { TraceLinkTable, TraceLinkGenerator } from "@/components/traceLink";
import { ProjectDisplay } from "@/components/project/";
import ModelTable from "./ModelTable.vue";

/**
 * Tabs for predicting and approving trace links.
 */
export default Vue.extend({
  name: "TracePredictionTabs",
  components: {
    ProjectDisplay,
    TraceLinkGenerator,
    ModelTable,
    TraceLinkTable,
    TabList,
    Typography,
  },
  props: {},
  data() {
    return {
      tab: 0,
      tabs: tracePredictionTabOptions(),
    };
  },
  computed: {},
  methods: {},
});
</script>

<style scoped lang="scss"></style>
