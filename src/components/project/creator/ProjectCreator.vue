<template>
  <v-container>
    <v-tabs v-model="tab">
      <v-tab v-for="{ name } in tabs" :key="name">
        <typography :value="name" />
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab" class="mt-1">
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
    </v-tabs-items>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { CreatorTypes } from "@/types";
import { getParam, QueryParams, updateParam } from "@/router";
import Typography from "@/components/common/display/Typography.vue";
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
    Typography,
    GitHubCreatorStepper,
    ProjectCreatorStepper,
    ProjectBulkUpload,
    JiraCreatorStepper,
  },
  data() {
    return {
      tab: 0,
      tabs: [
        { id: CreatorTypes.standard, name: "Standard Upload" },
        { id: CreatorTypes.bulk, name: "Bulk Upload" },
        { id: CreatorTypes.jira, name: "Jira Upload" },
        { id: CreatorTypes.github, name: "GitHub Upload" },
      ],
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
