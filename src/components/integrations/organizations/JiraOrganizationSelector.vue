<template>
  <stepper-list-step
    title="Jira Organizations"
    empty-message="There are no organizations."
    :item-count="organizations.length"
    :loading="loading"
  >
    <list>
      <list-item
        v-for="item in organizations"
        :key="item.name"
        :title="item.name"
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
import { watch, ref, onMounted } from "vue";
import { JiraOrganizationSchema } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleLoadJiraOrganizations } from "@/api";
import { StepperListStep, List, ListItem } from "@/components/common";

const organizations = ref<JiraOrganizationSchema[]>([]);
const loading = ref(false);

/**
 * Reloads the organizations list.
 */
function handleReload(): void {
  if (!integrationsStore.validJiraCredentials) return;

  integrationsStore.jiraOrganization = undefined;
  loading.value = true;

  handleLoadJiraOrganizations({
    onSuccess: (jiraOrganizations) => {
      organizations.value = jiraOrganizations;
    },
    onComplete: () => (loading.value = false),
  });
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
