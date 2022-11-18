<template>
  <generic-stepper-list-step
    empty-message="There are no projects."
    :item-count="projects.length"
    :loading="projectsLoading"
    title="Jira Projects"
  >
    <template slot="items">
      <template v-for="project in projects">
        <v-list-item :key="project.id" @click="handleProjectSelect(project)">
          <v-list-item-icon>
            <v-avatar>
              <img :src="project.mediumAvatarUrl" :alt="project.name" />
            </v-avatar>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="project.name" />

            <v-list-item-subtitle v-text="getProjectSubtitle(project)" />
          </v-list-item-content>
        </v-list-item>
      </template>
    </template>
  </generic-stepper-list-step>
</template>

<script lang="ts">
import Vue from "vue";
import { JiraProjectModel } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleLoadJiraProjects } from "@/api";
import { GenericStepperListStep } from "@/components";

/**
 * Allows for selecting a jira project.
 */
export default Vue.extend({
  name: "JiraProjectSelector",
  components: {
    GenericStepperListStep,
  },
  data() {
    return {
      projects: [] as JiraProjectModel[],
      projectsLoading: false,
    };
  },
  mounted() {
    if (!integrationsStore.validJiraCredentials) return;

    this.loadProjects();
  },
  computed: {
    /**
     * @return Whether there are current valid credentials.
     */
    hasCredentials(): boolean {
      return integrationsStore.validJiraCredentials;
    },
  },
  watch: {
    /**
     * Loads projects when credentials are valid.
     */
    hasCredentials(valid: boolean): void {
      if (!valid) return;

      this.loadProjects();
    },
  },
  methods: {
    /**
     * Loads a user's Jira projects for a selected site.
     */
    async loadProjects() {
      integrationsStore.jiraProject = undefined;
      this.projectsLoading = true;

      handleLoadJiraProjects({
        onSuccess: (projects) => {
          this.projects = projects;
          this.projectsLoading = false;
        },
        onError: () => (this.projectsLoading = false),
      });
    },
    /**
     * Returns a project's subtitle.
     * @param project - The project to extract from.
     * @return The subtitle.
     */
    getProjectSubtitle(project: JiraProjectModel): string {
      return project.key;
    },
    /**
     * Handles a click to select a project.
     * @param project - The project to select.
     */
    handleProjectSelect(project: JiraProjectModel | undefined) {
      integrationsStore.selectJiraProject(project);
    },
  },
});
</script>
