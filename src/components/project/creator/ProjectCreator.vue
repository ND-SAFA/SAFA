<template>
  <v-container>
    <v-tabs v-model="tab">
      <v-tab v-for="{ name } in tabs" :key="name">
        {{ name }}
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
import { getParam, QueryParams, updateParam } from "@/router";
import {
  ProjectCreatorStepper,
  JiraCreatorStepper,
  ProjectBulkUpload,
} from "./workflows";
import GitHubCreatorStepper from "@/components/project/creator/workflows/GitHubCreatorStepper.vue";

/**
 * Allows for creating a project.
 */
export default Vue.extend({
  name: "ProjectCreator",
  components: {
    GitHubCreatorStepper,
    ProjectCreatorStepper,
    ProjectBulkUpload,
    JiraCreatorStepper,
  },
  data() {
    return {
      tab: 0,
      tabs: [
        { id: "standard", name: "Standard Upload" },
        { id: "bulk", name: "Bulk Upload" },
        { id: "jira", name: "Jira Upload" },
        { id: "github", name: "GitHub Upload" },
      ],
    };
  },
  /**
   * When the page loads, switch to any set tab in the query.
   */
  mounted() {
    const tabId = getParam(QueryParams.TAB);
    const tabIndex = this.tabs.findIndex(({ id }) => id === tabId);

    if (!tabId || tabIndex === -1) return;

    this.tab = tabIndex;
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
  },
});
</script>
