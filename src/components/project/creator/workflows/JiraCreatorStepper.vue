<template>
  <generic-stepper
    v-model="currentStep"
    :steps="steps"
    submitText="Create Project"
    @submit="handleSaveProject"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <jira-authentication />
      </v-stepper-content>
      <v-stepper-content step="2">
        <jira-project-selector />
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import { JiraProjectModel, StepState } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleImportJiraProject } from "@/api";
import { GenericStepper } from "@/components/common";
import {
  JiraAuthentication,
  JiraProjectSelector,
} from "@/components/integrations";

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
      steps: [
        ["Connect to Jira", false],
        ["Select Project", false],
      ] as StepState[],
      currentStep: 1,
    };
  },
  computed: {
    /**
     * @return Whether there are current valid credentials.
     */
    hasCredentials(): boolean {
      return integrationsStore.validJiraCredentials;
    },
    /**
     * @return The current selected Jira project.
     */
    selectedProject(): JiraProjectModel | undefined {
      return integrationsStore.jiraProject;
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
    selectedProject(project: JiraProjectModel | undefined): void {
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
     * Attempts to import a Jira project.
     */
    handleSaveProject(): void {
      handleImportJiraProject({});
    },
  },
});
</script>
