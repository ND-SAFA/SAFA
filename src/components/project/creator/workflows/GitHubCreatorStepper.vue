<template>
  <generic-stepper
    v-model="currentStep"
    :steps="steps"
    submitText="Create Project"
    @submit="handleSaveProject"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <git-hub-authentication />
      </v-stepper-content>
      <v-stepper-content step="2">
        <git-hub-project-selector @select="handleProjectSelect($event)" />
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import { GitHubProjectModel, StepState } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleImportGitHubProject } from "@/api";
import { GenericStepper } from "@/components/common";
import {
  GitHubAuthentication,
  GitHubProjectSelector,
} from "@/components/integrations";

/**
 * Allows for creating a project from GitHub.
 */
export default Vue.extend({
  name: "GitHubCreatorStepper",
  components: {
    GitHubProjectSelector,
    GenericStepper,
    GitHubAuthentication,
  },
  data() {
    return {
      selectedRepository: undefined as GitHubProjectModel | undefined,
      steps: [
        ["Connect to GitHub", false],
        ["Select Repository", false],
      ] as StepState[],
      currentStep: 1,
    };
  },
  computed: {
    /**
     * @return Whether there are current valid credentials.
     */
    hasCredentials(): boolean {
      return integrationsStore.validGitHubCredentials;
    },
  },
  watch: {
    /**
     * Updates the current step when credentials are loaded.
     */
    hasCredentials(valid: boolean): void {
      if (valid) {
        this.currentStep = 2;
        this.setStepIsValid(0, true);
      } else {
        this.currentStep = 1;
        this.setStepIsValid(0, false);
      }
    },
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
      this.selectedRepository = undefined;
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
