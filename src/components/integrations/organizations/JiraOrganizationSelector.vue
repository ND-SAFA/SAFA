<template>
  <stepper-list-step
    title="Jira Organizations"
    empty-message="There are no organizations."
    :item-count="jiraApiStore.organizationList.length"
    :loading="jiraApiStore.loading"
  >
    <list>
      <list-item
        v-for="item in jiraApiStore.organizationList"
        :key="item.name"
        :title="item.name"
        clickable
        @click="handleOrganizationSelect(item)"
      />
    </list>
  </stepper-list-step>
</template>

<script lang="ts">
/**
 * Allows for selecting a jira organization.
 */
export default {
  name: "JiraOrganizationSelector",
};
</script>

<script setup lang="ts">
import { watch, onMounted } from "vue";
import { JiraOrganizationSchema } from "@/types";
import { integrationsStore, jiraApiStore } from "@/hooks";
import { StepperListStep, List, ListItem } from "@/components/common";

/**
 * Reloads the organizations list.
 */
function handleReload(): void {
  if (!integrationsStore.validJiraCredentials) return;

  jiraApiStore.handleLoadOrganizations();
}

/**
 * Handles a click to select an organization.
 * @param jiraOrganization - The organization to select.
 */
function handleOrganizationSelect(
  jiraOrganization: JiraOrganizationSchema | undefined
) {
  integrationsStore.selectJiraOrganization(jiraOrganization);
}

onMounted(() => handleReload());

watch(
  () => integrationsStore.validGitHubCredentials,
  () => handleReload()
);
</script>
