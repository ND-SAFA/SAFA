<template>
  <stepper-list-step
    empty-message="There are no projects."
    :item-count="projects.length"
    :loading="projectsLoading"
    title="Jira Projects"
  >
    <template v-for="project in projects" :key="project.id">
      <v-list-item @click="handleProjectSelect(project)">
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
  </stepper-list-step>
</template>

<script lang="ts">
import Vue from "vue";
import { JiraProjectSchema } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleLoadJiraProjects } from "@/api";
import { StepperListStep } from "@/components";

/**
 * Allows for selecting a jira project.
 */
export default Vue.extend({
  name: "JiraProjectSelector",
  components: {
    StepperListStep,
  },
  data() {
    return {
      projects: [] as JiraProjectSchema[],
      projectsLoading: false,
    };
  },
  computed: {
    /**
     * @return Whether there are current valid credentials.
     */
    hasCredentials(): boolean {
      return !!integrationsStore.jiraOrganization;
    },
  },
  watch: {
    /**
     * Loads projects when credentials are valid.
     */
    hasCredentials(): void {
      this.loadProjects();
    },
  },
  mounted() {
    this.loadProjects();
  },
  methods: {
    /**
     * Loads a user's Jira projects for a selected site.
     */
    async loadProjects() {
      if (!integrationsStore.jiraOrganization) return;

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
    getProjectSubtitle(project: JiraProjectSchema): string {
      return project.key;
    },
    /**
     * Handles a click to select a project.
     * @param project - The project to select.
     */
    handleProjectSelect(project: JiraProjectSchema | undefined) {
      integrationsStore.selectJiraProject(project);
    },
  },
});
</script>
