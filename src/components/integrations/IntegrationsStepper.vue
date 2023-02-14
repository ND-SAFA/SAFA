<template>
  <stepper
    v-model="currentStep"
    :minimal="type === 'connect'"
    :steps="steps"
    @submit="handleSaveProject"
  >
    <template #items>
      <v-stepper-content step="1">
        <authentication-selector v-model="source" />
      </v-stepper-content>
      <v-stepper-content step="2">
        <jira-organization-selector v-if="source === 'Jira'" />
        <git-hub-organization-selector v-if="source === 'GitHub'" />
      </v-stepper-content>
      <v-stepper-content step="3">
        <jira-project-selector v-if="source === 'Jira'" />
        <git-hub-project-selector v-if="source === 'GitHub'" />
      </v-stepper-content>
    </template>
  </stepper>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { StepState } from "@/types";
import { integrationsStore } from "@/hooks";
import {
  handleImportGitHubProject,
  handleImportJiraProject,
  handleSyncInstallation,
} from "@/api";
import { Stepper } from "@/components/common";
import {
  JiraOrganizationSelector,
  GitHubOrganizationSelector,
} from "./organizations";
import { AuthenticationSelector } from "./authentication";
import { JiraProjectSelector, GitHubProjectSelector } from "./projects";

/**
 * Allows for creating a project from integrations sources.
 *
 * @emits-1 `submit` - On project submission.
 */
export default defineComponent({
  name: "IntegrationsStepper",
  components: {
    JiraOrganizationSelector,
    GitHubOrganizationSelector,
    AuthenticationSelector,
    GitHubProjectSelector,
    JiraProjectSelector,
    Stepper,
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
      steps: [
        ["Connect to Source", false],
        ["Select Organization", false],
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
     * @return What organization is selected.
     */
    organizationIsSelected(): string | undefined {
      if (this.source === "Jira") {
        return integrationsStore.jiraOrganization?.name;
      } else if (this.source === "GitHub") {
        return integrationsStore.gitHubOrganization?.name;
      } else {
        return undefined;
      }
    },
    /**
     * @return Whether a project is selected.
     */
    projectIsSelected(): string | undefined {
      if (this.source === "Jira") {
        return integrationsStore.jiraProject?.name;
      } else if (this.source === "GitHub") {
        return integrationsStore.gitHubProject?.name;
      } else {
        return undefined;
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
    organizationIsSelected(name: string | undefined): void {
      if (name) {
        this.currentStep = 3;
        this.setStepIsValid(1, true);
      } else {
        this.currentStep = 2;
        this.setStepIsValid(1, false);
      }
    },
    /**
     * Updates the selection step when a project is selected.
     */
    projectIsSelected(name: string | undefined): void {
      this.setStepIsValid(2, !!name);
    },
  },
  methods: {
    /**
     * Sets the valid state of a step.
     * @param stepIndex - The step cto change.
     * @param isValid - Whether the step is valid.
     */
    setStepIsValid(stepIndex: number, isValid: boolean): void {
      this.steps[stepIndex] = [this.steps[stepIndex][0], isValid];
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
              installationOrgId: integrationsStore.jiraOrganization?.id || "",
              installationId: integrationsStore.jiraProject?.id || "",
            },
            callbacks
          );
        } else if (this.source === "GitHub") {
          handleSyncInstallation(
            {
              type: "GITHUB",
              installationOrgId: integrationsStore.gitHubOrganization?.id || "",
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
