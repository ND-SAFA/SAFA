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
          :has-credentials="validCredentials"
          :is-loading="isLoading"
          @delete="handleDeleteCredentials"
        />
      </v-stepper-content>

      <v-stepper-content step="2">
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
import { JiraProjectModel, StepState } from "@/types";
import { getParam, QueryParams } from "@/router";
import { deleteJiraCredentials, handleImportJiraProject } from "@/api";
import { GenericStepper } from "@/components/common";
import {
  JiraAuthentication,
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
    JiraAuthentication,
    GenericStepper,
  },
  data() {
    return {
      accessCode: getParam(QueryParams.JIRA_TOKEN),
      isLoading: true,
      validCredentials: false,

      projects: [] as JiraProjectModel[],
      projectsLoading: false,
      selectedProject: undefined as JiraProjectModel | undefined,

      steps: [
        ["Connect to Jira", false],
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
      onSuccess: () => {
        this.isLoading = false;
        this.validCredentials = true;
        this.currentStep = 2;
        this.setStepIsValid(0, true);
        this.loadProjects();
      },
      onError: () => {
        this.isLoading = false;
        this.validCredentials = false;
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
      this.validCredentials = false;
      this.projects = [];
    },
    /**
     * Clears the saved credentials
     */
    async handleDeleteCredentials(): Promise<void> {
      await deleteJiraCredentials();
      this.validCredentials = false;
      this.currentStep = 1;
    },
    /**
     * Loads a user's Jira projects for a selected site.
     */
    async loadProjects() {
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
     * Selects a Jira project to import.
     */
    handleProjectSelect(project: JiraProjectModel) {
      if (this.selectedProject?.id !== project.id) {
        this.selectedProject = project;
        this.setStepIsValid(1, true);
      } else {
        this.selectedProject = undefined;
        this.setStepIsValid(1, false);
      }
    },
    /**
     * Attempts to import a Jira project.
     */
    handleSaveProject(): void {
      if (!this.selectedProject) return;

      handleImportJiraProject(this.selectedProject.id, {
        onSuccess: () => this.clearData(),
      });
    },
  },
});
</script>
