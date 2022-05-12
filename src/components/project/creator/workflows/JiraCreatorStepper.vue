<template>
  <generic-stepper
    v-model="currentStep"
    :steps="steps"
    submitText="Create Project"
    @submit="handleSaveProject()"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <jira-authentication :token="token" :is-loading="isLoading" />
      </v-stepper-content>

      <v-stepper-content step="2">
        <jira-site-selector
          :loading="sitesLoading"
          :sites="sites"
          @select="handleSiteSelect($event)"
        />
      </v-stepper-content>

      <v-stepper-content step="3">
        <jira-project-selector
          :loading="projectsLoading"
          :projects="projects"
          @select="handleProjectSelect($event)"
        />
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import {
  JiraAccessToken,
  JiraCloudSite,
  JiraProject,
  StepState,
} from "@/types";
import { getParam, QueryParams } from "@/router";
import { getJiraCloudSites, handleImportJiraProject } from "@/api";
import { GenericStepper } from "@/components/common";
import {
  JiraAuthentication,
  JiraSiteSelector,
  JiraProjectSelector,
} from "@/components/project/creator/steps";
import {
  handleAuthorizeJira,
  handleLoadJiraProjects,
} from "@/api/handlers/integration-handler";

/**
 * Allows for creating a project from Jira.
 */
export default Vue.extend({
  name: "JiraCreatorStepper",
  components: {
    JiraProjectSelector,
    JiraSiteSelector,
    JiraAuthentication,
    GenericStepper,
  },
  data() {
    return {
      accessCode: getParam(QueryParams.JIRA_TOKEN),
      token: undefined as JiraAccessToken | undefined,
      isLoading: true,

      sites: [] as JiraCloudSite[],
      sitesLoading: false,
      selectedSite: undefined as JiraCloudSite | undefined,

      projects: [] as JiraProject[],
      projectsLoading: false,
      selectedProject: undefined as JiraProject | undefined,

      steps: [
        ["Connect to Jira", false],
        ["Select Domain", false],
        ["Select Project", false],
      ] as StepState[],
      currentStep: 1,
    };
  },
  /**
   * If a jira access code is found in the query, loads the Jira authorization token and sites for the user.
   */
  mounted() {
    handleAuthorizeJira(this.accessCode, {
      onSuccess: (token) => {
        this.isLoading = false;
        this.token = token;
        this.currentStep = 2;
        this.setStepIsValid(0, true);
        this.loadSites();
      },
      onError: () => {
        this.isLoading = false;
      },
    });
  },
  methods: {
    /**
     * Sets the valid state of a step.
     * @param stepIndex - The step cto change.
     * @param isValid - Whether the step is valid.
     */
    setStepIsValid(stepIndex: number, isValid: boolean): void {
      Vue.set(this.steps, stepIndex, [this.steps[stepIndex][0], isValid]);
    },
    /**
     * Clears stepper data.
     */
    clearData(): void {
      this.token = undefined;
      this.sites = [];
      this.projects = [];
    },
    /**
     * Loads a user's Jira sites.
     */
    async loadSites() {
      if (!this.token) return;

      this.sitesLoading = true;
      this.sites = await getJiraCloudSites(this.token.access_token);
      this.sitesLoading = false;
    },
    /**
     * Loads a user's Jira projects for a selected site.
     */
    async loadProjects() {
      if (!this.selectedSite || !this.token) return;

      this.projectsLoading = true;

      handleLoadJiraProjects(this.token, this.selectedSite.id, {
        onSuccess: (projects) => {
          this.projects = projects;
          this.projectsLoading = false;
        },
        onError: () => (this.projectsLoading = false),
      });
    },
    /**
     * Selects a Jira site to load projects from.
     */
    handleSiteSelect(site: JiraCloudSite) {
      if (this.selectedSite?.id !== site.id) {
        this.selectedSite = site;
        this.setStepIsValid(1, true);
        this.currentStep = 3;
        this.loadProjects();
      } else {
        this.selectedSite = undefined;
        this.setStepIsValid(1, false);
      }
    },
    /**
     * Selects a Jira project to import.
     */
    handleProjectSelect(project: JiraProject) {
      if (this.selectedProject?.id !== project.id) {
        this.selectedProject = project;
        this.setStepIsValid(2, true);
      } else {
        this.selectedProject = undefined;
        this.setStepIsValid(2, false);
      }
    },
    /**
     * Attempts to import a jira project.
     */
    handleSaveProject(): void {
      if (!this.token || !this.selectedSite || !this.selectedProject) return;

      handleImportJiraProject(this.selectedProject.id, {
        onSuccess: () => this.clearData(),
      });
    },
  },
});
</script>
