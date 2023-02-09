<template>
  <v-container>
    <typography t="4" el="h1" variant="title" value="Create Project" />
    <v-divider />
    <typography
      el="p"
      y="2"
      value="Create a project using one of the following methods."
    />
    <tab-list v-model="tab" :tabs="tabs">
      <v-tab key="1">
        <project-creator-stepper />
      </v-tab>
      <v-tab key="2">
        <project-bulk-upload />
      </v-tab>
      <v-tab key="3">
        <integrations-stepper type="create" />
      </v-tab>
    </tab-list>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { creatorTabOptions } from "@/util";
import { getParam, QueryParams, updateParam } from "@/router";
import { TabList, Typography } from "@/components/common";
import { IntegrationsStepper } from "@/components/integrations";
import { ProjectCreatorStepper, ProjectBulkUpload } from "./workflows";

/**
 * Allows for creating a project.
 */
export default Vue.extend({
  name: "ProjectCreator",
  components: {
    IntegrationsStepper,
    TabList,
    ProjectCreatorStepper,
    ProjectBulkUpload,
    Typography,
  },
  data() {
    return {
      tab: 0,
      tabs: creatorTabOptions(),
    };
  },
  watch: {
    /**
     * When the tab changes, update the query tab id.
     */
    tab(index: number) {
      const currentTabId = this.tabs[index].id;
      const routeTabId = getParam(QueryParams.TAB);

      if (currentTabId !== routeTabId) {
        updateParam(QueryParams.TAB, currentTabId);
      }
    },
    /**
     * Opens the current tab when the route changes.
     */
    $route() {
      this.openCurrentTab();
    },
  },
  /**
   * When the page loads, switch to any set tab in the query.
   */
  mounted() {
    this.openCurrentTab();
  },
  methods: {
    /**
     * Switch to any set tab in the query.
     */
    openCurrentTab() {
      const tabId = getParam(QueryParams.TAB);
      const tabIndex = this.tabs.findIndex(({ id }) => id === tabId);

      if (!tabId || tabIndex === -1 || this.tab === tabIndex) return;

      this.tab = tabIndex;
    },
  },
});
</script>
