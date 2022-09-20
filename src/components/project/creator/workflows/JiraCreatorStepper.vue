<template>
  <generic-stepper
    v-model="currentStep"
    :steps="steps"
    submitText="Create Project"
    @submit="handleSaveProject()"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <jira-authentication
          :has-credentials="!!credentials"
          :is-loading="isLoading"
        />
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
  InternalJiraCredentialsModel,
  JiraCloudSiteModel,
  JiraProjectModel,
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
} from "@/api/handlers/project/integration-handler";

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
      credentials: undefined as InternalJiraCredentialsModel | undefined,
      isLoading: true,

      sites: [] as JiraCloudSiteModel[],
      sitesLoading: false,
      selectedSite: undefined as JiraCloudSiteModel | undefined,

      projects: [] as JiraProjectModel[],
      projectsLoading: false,
      selectedProject: undefined as JiraProjectModel | undefined,

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
      onSuccess: (credentials) => {
        this.isLoading = false;
        this.credentials = credentials;
        this.loadSites();
        this.setStepIsValid(0, true);

        if (credentials.cloudId) {
          this.currentStep = 3;
          this.setStepIsValid(1, true);
          this.loadProjects();
        } else {
          this.currentStep = 2;
        }
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
      this.credentials = undefined;
      this.sites = [];
      this.projects = [];
    },
    /**
     * Loads a user's Jira sites.
     */
    async loadSites() {
      if (!this.credentials) return;

      this.sitesLoading = true;
      this.sites = await getJiraCloudSites(this.credentials.bearerAccessToken);
      this.sitesLoading = false;
    },
    /**
     * Loads a user's Jira projects for a selected site.
     */
    async loadProjects() {
      if (!this.credentials) return;

      if (this.selectedSite) {
        this.credentials.cloudId = this.selectedSite.id;
      }

      this.projectsLoading = true;
      handleLoadJiraProjects(this.credentials, {
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
    handleSiteSelect(site: JiraCloudSiteModel) {
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
    handleProjectSelect(project: JiraProjectModel) {
      if (this.selectedProject?.id !== project.id) {
        this.selectedProject = project;
        this.setStepIsValid(2, true);
      } else {
        this.selectedProject = undefined;
        this.setStepIsValid(2, false);
      }
    },
    /**
     * Attempts to import a Jira project.
     */
    handleSaveProject(): void {
      if (!this.credentials || !this.selectedProject) return;

      handleImportJiraProject(
        this.credentials.cloudId,
        this.selectedProject.id,
        {
          onSuccess: () => this.clearData(),
        }
      );
    },
  },
});
</script>
