<template>
  <v-container>
    <tab-list v-model="tab" :tabs="tabs">
      <v-tab-item key="1">
        <project-creator-stepper />
      </v-tab-item>
      <v-tab-item key="2">
        <project-bulk-upload />
      </v-tab-item>
      <v-tab-item key="3">
        <jira-creator-stepper />
      </v-tab-item>
      <v-tab-item key="4">
        <git-hub-creator-stepper />
      </v-tab-item>
    </tab-list>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { creatorTabOptions } from "@/util";
import { getParam, QueryParams, updateParam } from "@/router";
import { TabList } from "@/components/common";
import {
  ProjectCreatorStepper,
  JiraCreatorStepper,
  GitHubCreatorStepper,
  ProjectBulkUpload,
} from "./workflows";

/**
 * Allows for creating a project.
 */
export default Vue.extend({
  name: "ProjectCreator",
  components: {
    TabList,
    GitHubCreatorStepper,
    ProjectCreatorStepper,
    ProjectBulkUpload,
    JiraCreatorStepper,
  },
  data() {
    return {
      tab: 0,
      tabs: creatorTabOptions(),
    };
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
});
</script>
