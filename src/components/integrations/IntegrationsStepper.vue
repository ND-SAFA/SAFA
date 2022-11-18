<template>
  <generic-stepper
    :minimal="type === 'connect'"
    v-model="currentStep"
    :steps="steps"
    @submit="handleSaveProject"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <v-container style="max-width: 30em">
          <v-select
            filled
            label="Data Source"
            v-model="source"
            :items="sourceTypes"
          />
          <jira-authentication v-if="source === 'Jira'" />
          <git-hub-authentication v-if="source === 'GitHub'" />
        </v-container>
      </v-stepper-content>
      <v-stepper-content step="2">
        <jira-project-selector v-if="source === 'Jira'" />
        <git-hub-project-selector v-if="source === 'GitHub'" />
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { StepState } from "@/types";
import { integrationsStore } from "@/hooks";
import {
  handleImportGitHubProject,
  handleImportJiraProject,
  handleSyncInstallation,
} from "@/api";
import { GenericStepper } from "@/components/common";
import { GitHubAuthentication, JiraAuthentication } from "./authentication";
import { JiraProjectSelector, GitHubProjectSelector } from "./projects";

/**
 * Allows for creating a project from integrations sources.
 *
 * @emits-1 `submit` - On project submission.
 */
export default Vue.extend({
  name: "IntegrationsStepper",
  components: {
    GitHubProjectSelector,
    GitHubAuthentication,
    JiraProjectSelector,
    JiraAuthentication,
    GenericStepper,
  },
  props: {
    type: {
      required: true,
      type: String as PropType<"create" | "connect">,
    },
  },
  data() {
    return {
      source: undefined as "Jira" | "GitHub" | undefined,
      sourceTypes: ["Jira", "GitHub"],
      steps: [
        ["Connect to Source", false],
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
      if (this.source === "Jira") {
        return integrationsStore.validJiraCredentials;
      } else if (this.source === "GitHub") {
        return integrationsStore.validGitHubCredentials;
      } else {
        return false;
      }
    },
    /**
     * @return Whether a project is selected
     */
    projectIsSelected(): boolean {
      if (this.source === "Jira") {
        return !!integrationsStore.jiraProject;
      } else if (this.source === "GitHub") {
        return !!integrationsStore.gitHubProject;
      } else {
        return false;
      }
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
    projectIsSelected(selected: boolean): void {
      this.setStepIsValid(1, selected);
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
     * Attempts to import a project.
     */
    handleSaveProject(): void {
      const callbacks = {
        onSuccess: () => this.$emit("submit"),
      };

      if (this.type === "create") {
        // Create a new project.
        if (this.source === "Jira") {
          handleImportJiraProject(callbacks);
        } else if (this.source === "GitHub") {
          handleImportGitHubProject(callbacks);
        }
      } else {
        // Sync with the current project.
        if (this.source === "Jira") {
          handleSyncInstallation(
            {
              type: "JIRA",
              installationId: integrationsStore.jiraProject?.id || "",
            },
            callbacks
          );
        } else if (this.source === "GitHub") {
          handleSyncInstallation(
            {
              type: "GITHUB",
              installationId: integrationsStore.gitHubProject?.name || "",
            },
            callbacks
          );
        }
      }
    },
  },
});
</script>
