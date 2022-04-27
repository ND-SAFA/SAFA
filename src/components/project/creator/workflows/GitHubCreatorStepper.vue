<template>
  <generic-stepper
    v-model="currentStep"
    :steps="steps"
    submitText="Create Project"
    @submit="handleSaveProject()"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <p class="mx-auto text-caption" style="width: fit-content">
          This page is a work in progress.
        </p>
      </v-stepper-content>

      <v-stepper-content step="2">
        <p class="mx-auto text-caption" style="width: fit-content">
          [Select an Organization.]
        </p>
      </v-stepper-content>

      <v-stepper-content step="3">
        <p class="mx-auto text-caption" style="width: fit-content">
          [Select a Project.]
        </p>
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import { StepState } from "@/types";
import { handleImportGitHubProject } from "@/api";
import { GenericStepper } from "@/components/common";

// TODO: properly define and remove.
type GitHubOrganization = Record<string, any>;
type GitHubProject = Record<string, any>;

/**
 * Allows for creating a project from GitHub.
 */
export default Vue.extend({
  name: "GitHubCreatorStepper",
  components: {
    GenericStepper,
  },
  data() {
    return {
      accessCode: "",
      token: "",

      organizations: [] as GitHubOrganization[],
      organizationsLoading: false,
      selectedOrganization: undefined as GitHubOrganization | undefined,

      projects: [] as GitHubProject[],
      projectsLoading: false,
      selectedProject: undefined as GitHubProject | undefined,

      steps: [
        ["Connect to GitHub", false],
        ["Select Organization", false],
        ["Select Project", false],
      ] as StepState[],
      currentStep: 1,
    };
  },
  /**
   * TODO
   * If a jira access code is found in the query, loads the Jira authorization token and sites for the user.
   */
  mounted() {
    console.log("This will load github authentication redirects.");
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
     * TODO
     * Clears stepper data.
     */
    clearData(): void {
      console.log("This will clear data.");
    },
    /**
     * TODO
     * Loads a GitHub authorization token.
     */
    async loadToken() {
      this.token = "";
    },
    /**
     * TODO
     * Loads a user's GitHub organizations.
     */
    async loadOrganizations() {
      this.selectedOrganization = undefined;
    },
    /**
     * TODO
     * Loads a user's GitHub projects for a selected organization.
     */
    async loadProjects() {
      this.selectedProject = undefined;
    },
    /**
     * TODO
     * Selects a GitHub organization to load projects from.
     */
    handleOrganizationSelect(org: GitHubOrganization) {
      if (this.selectedOrganization?.id !== org.id) {
        this.selectedOrganization = org;
        this.setStepIsValid(1, true);
        this.currentStep = 3;
        this.loadProjects();
      } else {
        this.selectedOrganization = undefined;
        this.setStepIsValid(1, false);
      }
    },
    /**
     * TODO
     * Selects a GitHub project to import.
     */
    handleProjectSelect(project: GitHubProject) {
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
      if (!this.token || !this.selectedOrganization || !this.selectedProject)
        return;

      handleImportGitHubProject(
        this.token,
        this.selectedOrganization.id,
        this.selectedProject.id,
        {
          onSuccess: () => this.clearData(),
        }
      );
    },
  },
});
</script>
