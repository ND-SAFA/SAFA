<template>
  <git-hub-project-input v-if="props.source === 'GitHub'" />
  <jira-project-input v-if="props.source === 'Jira'" />
</template>

<script lang="ts">
/**
 * Allows for configuring imports once a source has been selected.
 */
export default {
  name: "IntegrationSelector",
};
</script>

<script setup lang="ts">
import { onMounted, watch } from "vue";
import { gitHubApiStore, integrationsStore, jiraApiStore } from "@/hooks";
import {
  GitHubProjectInput,
  JiraProjectInput,
} from "@/components/integrations";

const props = defineProps<{ source: "Jira" | "GitHub" }>();

/**
 * Reloads integrations data.
 */
function handleReloadIntegrations() {
  if (integrationsStore.validJiraCredentials) {
    jiraApiStore.handleLoadOrganizations();
  }
  if (integrationsStore.validGitHubCredentials) {
    gitHubApiStore.handleLoadProjects();
  }
}

onMounted(() => handleReloadIntegrations());

watch(
  () => [
    integrationsStore.validJiraCredentials,
    integrationsStore.validGitHubCredentials,
  ],
  () => handleReloadIntegrations()
);
</script>
