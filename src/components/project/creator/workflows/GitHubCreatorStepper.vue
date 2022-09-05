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
          :has-credentials="!!credentials"
          :is-loading="isLoading"
        />
      </v-stepper-content>

      <v-stepper-content step="2">
        <git-hub-installation-selector
          :installations="installations"
          :loading="installationsLoading"
          @select="handleInstallationSelect($event)"
        />
      </v-stepper-content>

      <v-stepper-content step="3">
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
import {
  GitHubInstallationModel,
  GitHubRepositoryModel,
  StepState,
  InternalGitHubCredentialsModel,
} from "@/types";
import { getParam, QueryParams } from "@/router";
import {
  getGitHubInstallations,
  getGitHubRepositories,
  handleImportGitHubProject,
  handleLoadGitHubProjects,
} from "@/api";
import { handleAuthorizeGitHub } from "@/api/handlers/project/integration-handler";
import { GenericStepper } from "@/components/common";
import {
  GitHubAuthentication,
  GitHubRepositorySelector,
  GitHubInstallationSelector,
} from "@/components/project/creator/steps";

/**
 * Allows for creating a project from GitHub.
 */
export default Vue.extend({
  name: "GitHubCreatorStepper",
  components: {
    GitHubRepositorySelector,
    GitHubInstallationSelector,
    GenericStepper,
    GitHubAuthentication,
  },
  data() {
    return {
      accessCode: getParam(QueryParams.GITHUB_TOKEN),
      credentials: undefined as InternalGitHubCredentialsModel | undefined,
      isLoading: true,

      installations: [] as GitHubInstallationModel[],
      installationsLoading: false,
      selectedInstallation: undefined as GitHubInstallationModel | undefined,

      repositories: [] as GitHubRepositoryModel[],
      repositoriesLoading: false,
      selectedRepository: undefined as GitHubRepositoryModel | undefined,

      steps: [
        ["Connect to GitHub", false],
        ["Select Installation", false],
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
      onSuccess: (credentials) => {
        this.credentials = credentials;
        this.isLoading = false;
        this.currentStep = 2;
        this.setStepIsValid(0, true);
        this.loadInstallations();
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
      this.installations = [];
      this.repositories = [];
    },
    /**
     * Loads a user's GitHub organizations.
     */
    async loadInstallations() {
      if (!this.credentials) return;

      this.installationsLoading = true;
      this.installations = await getGitHubInstallations(
        this.credentials.accessToken
      );
      this.installationsLoading = false;
    },
    /**
     * Loads a user's GitHub projects for a selected organization.
     */
    async loadProjects() {
      if (!this.credentials || !this.selectedInstallation) return;

      if (this.selectedInstallation) {
        this.credentials.installationId = this.selectedInstallation.id;
      }

      this.repositoriesLoading = true;
      handleLoadGitHubProjects(this.credentials, {
        onSuccess: (repositories) => {
          this.repositories = repositories;
          this.repositoriesLoading = false;
        },
        onError: () => (this.repositoriesLoading = false),
      });
    },
    /**
     * Selects a GitHub organization to load projects from.
     */
    handleInstallationSelect(org: GitHubInstallationModel) {
      if (this.selectedInstallation?.id !== org.id) {
        this.selectedInstallation = org;
        this.setStepIsValid(1, true);
        this.currentStep = 3;
        this.loadProjects();
      } else {
        this.selectedInstallation = undefined;
        this.setStepIsValid(1, false);
      }
    },
    /**
     * Selects a GitHub project to import.
     */
    handleProjectSelect(project: GitHubRepositoryModel) {
      if (this.selectedRepository?.id !== project.id) {
        this.selectedRepository = project;
        this.setStepIsValid(2, true);
      } else {
        this.selectedRepository = undefined;
        this.setStepIsValid(2, false);
      }
    },
    /**
     * Attempts to import a GitHub project.
     */
    handleSaveProject(): void {
      if (
        !this.credentials ||
        !this.selectedInstallation ||
        !this.selectedRepository
      )
        return;

      handleImportGitHubProject(this.selectedRepository.id, {
        onSuccess: () => this.clearData(),
      });
    },
  },
});
</script>
