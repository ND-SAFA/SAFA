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
        <jira-upload />
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { navigateTo, router, Routes } from "@/router";
import { JiraUpload, ProjectBulkUpload } from "./panels";
import ProjectCreatorStepper from "./ProjectCreatorStepper.vue";

/**
 * Allows for creating a project.
 */
export default Vue.extend({
  components: { ProjectCreatorStepper, ProjectBulkUpload, JiraUpload },
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
    const { query } = router.currentRoute;

    if (query.tab) {
      this.tab = this.tabs.findIndex(({ id }) => id === query.tab);
    }
  },
  watch: {
    tab(index: number) {
      const tabId = this.tabs[index].id;
      const { query } = router.currentRoute;

      if (query.tab !== tabId) {
        navigateTo(Routes.PROJECT_CREATOR, { tab: tabId });
      }
    },
  },
});
</script>
