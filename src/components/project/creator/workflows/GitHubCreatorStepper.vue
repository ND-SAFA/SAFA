<template>
  <generic-stepper
    v-model="currentStep"
    :steps="steps"
    submitText="Create Project"
    @submit="handleSaveProject()"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <git-hub-authentication
          :has-credentials="validCredentials"
          :is-loading="isLoading"
          @delete="handleDeleteCredentials"
        />
      </v-stepper-content>

      <v-stepper-content step="2">
        <git-hub-repository-selector
          :repositories="repositories"
          :loading="repositoriesLoading"
          @select="handleProjectSelect($event)"
        />
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import { GitHubProjectModel, StepState } from "@/types";
import { getParam, QueryParams } from "@/router";
import {
  deleteGitHubCredentials,
  handleImportGitHubProject,
  handleLoadGitHubProjects,
} from "@/api";
import { handleAuthorizeGitHub } from "@/api/handlers/project/integration-handler";
import { GenericStepper } from "@/components/common";
import {
  GitHubAuthentication,
  GitHubRepositorySelector,
} from "@/components/project/creator/steps";

/**
 * Allows for creating a project from GitHub.
 */
export default Vue.extend({
  name: "GitHubCreatorStepper",
  components: {
    GitHubRepositorySelector,
    GenericStepper,
    GitHubAuthentication,
  },
  data() {
    return {
      accessCode: getParam(QueryParams.GITHUB_TOKEN),
      isLoading: true,
      validCredentials: false,

      repositories: [] as GitHubProjectModel[],
      repositoriesLoading: false,
      selectedRepository: undefined as GitHubProjectModel | undefined,

      steps: [
        ["Connect to GitHub", false],
        ["Select Repository", false],
      ] as StepState[],
      currentStep: 1,
    };
  },
  /**
   * If a GitHub access code is found in the query, loads the GitHub authorization token and sites for the user.
   */
  mounted() {
    handleAuthorizeGitHub(this.accessCode, {
      onSuccess: () => {
        this.validCredentials = true;
        this.isLoading = false;
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
      this.repositories = [];
    },
    /**
     * Clears the saved credentials
     */
    async handleDeleteCredentials(): Promise<void> {
      await deleteGitHubCredentials();
      this.validCredentials = false;
      this.currentStep = 1;
    },
    /**
     * Loads a user's GitHub projects for a selected organization.
     */
    async loadProjects() {
      this.repositoriesLoading = true;
      handleLoadGitHubProjects({
        onSuccess: (repositories) => {
          this.repositories = repositories;
          this.repositoriesLoading = false;
        },
        onError: () => (this.repositoriesLoading = false),
      });
    },
    /**
     * Selects a GitHub project to import.
     */
    handleProjectSelect(project: GitHubProjectModel) {
      if (this.selectedRepository?.id !== project.id) {
        this.selectedRepository = project;
        this.setStepIsValid(1, true);
      } else {
        this.selectedRepository = undefined;
        this.setStepIsValid(1, false);
      }
    },
    /**
     * Attempts to import a GitHub project.
     */
    handleSaveProject(): void {
      if (!this.selectedRepository) return;

      handleImportGitHubProject(this.selectedRepository.name, {
        onSuccess: () => this.clearData(),
      });
    },
  },
});
</script>
