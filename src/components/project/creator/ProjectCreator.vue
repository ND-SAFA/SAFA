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
import { clearProject } from "@/api";

/**
 * Allows for creating a project.
 */
export default Vue.extend({
  components: { ProjectCreatorStepper, ProjectBulkUpload, JiraCreatorStepper },
  data() {
    return {
      tab: 0,
      tabs: [
        { id: "standard", name: "Standard Upload" },
        { id: "bulk", name: "Bulk Upload" },
        { id: "jira", name: "JIRA Upload" },
      ],
    };
  },
  mounted() {
    const tabId = getParam(QueryParams.TAB);
    const tabIndex = this.tabs.findIndex(({ id }) => id === tabId);

    if (tabId && tabIndex !== -1) {
      this.tab = tabIndex;
    }

    clearProject();
  },
  watch: {
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
