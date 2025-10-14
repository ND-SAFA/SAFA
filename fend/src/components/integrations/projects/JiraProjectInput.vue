<template>
  <div>
    <jira-authentication v-if="!integrationsStore.validJiraCredentials" />
    <select-input
      v-else
      v-model="integrationsStore.jiraOrganization"
      label="Jira Organization"
      :options="jiraApiStore.organizationList"
      :loading="jiraApiStore.loading"
      hint="Required"
      class="full-width"
      option-label="name"
      data-cy="input-github-organization"
    />
    <select-input
      v-if="!!integrationsStore.jiraOrganization"
      v-model="integrationsStore.jiraProject"
      label="Jira Project"
      :options="jiraApiStore.projectList"
      hint="Required"
      class="full-width"
      option-label="name"
      data-cy="input-github-project"
    />
  </div>
</template>

<script lang="ts">
/**
 * Allows for selecting a GitHub repository.
 */
export default {
  name: "GitHubProjectInput",
};
</script>

<script setup lang="ts">
import { computed, onMounted, watch } from "vue";
import { integrationsStore, jiraApiStore } from "@/hooks";
import { SelectInput } from "@/components/common";
import { JiraAuthentication } from "@/components/integrations/authentication";

const organizationName = computed(
  () => integrationsStore.jiraOrganization?.name
);

/**
 * Loads a user's GitHub projects for a selected organization.
 */
function handleReload() {
  if (!integrationsStore.jiraOrganization) return;

  jiraApiStore.handleLoadProjects();
}

onMounted(() => handleReload());

watch(
  () => organizationName.value,
  () => handleReload()
);
</script>
