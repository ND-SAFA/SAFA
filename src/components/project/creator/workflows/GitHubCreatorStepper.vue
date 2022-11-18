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
        <git-hub-project-selector />
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
    /**
     * @return The current selected GitHub project.
     */
    selectedProject(): GitHubProjectModel | undefined {
      return integrationsStore.gitHubProject;
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
    /**
     * Updates the selection step when a project is selected.
     */
    selectedProject(project: GitHubProjectModel | undefined): void {
      this.setStepIsValid(1, !!project);
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
     * Attempts to import a GitHub project.
     */
    handleSaveProject(): void {
      handleImportGitHubProject({});
    },
  },
});
</script>
