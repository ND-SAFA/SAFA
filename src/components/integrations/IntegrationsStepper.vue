<template>
  <panel-card>
    <stepper
      v-model="currentStep"
      :minimal="props.type === 'connect'"
      :steps="steps"
      @submit="handleSaveProject"
    >
      <template #1>
        <authentication-selector v-model="source" @input="handleSelectSource" />
      </template>
      <template #2>
        <jira-organization-selector v-if="source === 'Jira'" />
        <git-hub-organization-selector v-if="source === 'GitHub'" />
      </template>
      <template #3>
        <jira-project-selector v-if="source === 'Jira'" />
        <git-hub-project-selector v-if="source === 'GitHub'" />
      </template>
    </stepper>
  </panel-card>
</template>

<script lang="ts">
/**
 * Allows for creating a project from integrations sources.
 *
 * @emits-1 `submit` - On project submission.
 */
export default {
  name: "IntegrationsStepper",
};
</script>

<script setup lang="ts">
import { ref, watch } from "vue";
import { StepperStep } from "@/types";
import {
  createProjectApiStore,
  integrationsApiStore,
  integrationsStore,
} from "@/hooks";
import { Stepper, PanelCard } from "@/components/common";
import {
  JiraOrganizationSelector,
  GitHubOrganizationSelector,
} from "./organizations";
import { AuthenticationSelector } from "./authentication";
import { JiraProjectSelector, GitHubProjectSelector } from "./projects";

const props = defineProps<{
  type: "create" | "connect";
}>();

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const source = ref<"Jira" | "GitHub" | undefined>();
const currentStep = ref(1);
const steps = ref<StepperStep[]>([
  { title: "Connect to Source", done: false },
  { title: "Select Organization", done: false },
  { title: "Select Project", done: false },
]);

/**
 * Selects the type of integration to import from.
 * @param type - The type of integration.
 */
function handleSelectSource(type: "Jira" | "GitHub"): void {
  source.value = type;
}

/**
 * Attempts to import a project.
 */
function handleSaveProject(): void {
  const callbacks = {
    onSuccess: () => emit("submit"),
  };

  if (props.type === "create") {
    // Create a new project.
    if (source.value === "Jira") {
      createProjectApiStore.handleJiraImport(callbacks);
    } else if (source.value === "GitHub") {
      createProjectApiStore.handleGitHubImport(callbacks);
    }
  } else {
    // Sync with the current project.
    integrationsApiStore.handleNewSync(source.value, callbacks);
  }
}

watch(
  () => {
    if (source.value === "Jira") {
      return integrationsStore.validJiraCredentials;
    } else if (source.value === "GitHub") {
      return integrationsStore.validGitHubCredentials;
    } else {
      return false;
    }
  },
  (valid) => {
    if (valid) {
      currentStep.value = 2;
      steps.value[0].done = true;
    } else {
      currentStep.value = 1;
      steps.value[0].done = false;
    }
  }
);

watch(
  () => {
    if (source.value === "Jira") {
      return integrationsStore.jiraOrganization?.name;
    } else if (source.value === "GitHub") {
      return integrationsStore.gitHubOrganization?.name;
    } else {
      return undefined;
    }
  },
  (name) => {
    if (name) {
      currentStep.value = 3;
      steps.value[1].done = true;
    } else {
      currentStep.value = 2;
      steps.value[1].done = false;
    }
  }
);

watch(
  () => {
    if (source.value === "Jira") {
      return integrationsStore.jiraProject?.name;
    } else if (source.value === "GitHub") {
      return integrationsStore.gitHubProject?.name;
    } else {
      return undefined;
    }
  },
  (name) => {
    steps.value[2].done = !!name;
  }
);
</script>
