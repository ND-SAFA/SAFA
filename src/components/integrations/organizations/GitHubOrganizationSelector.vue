<template>
  <stepper-list-step
    title="GitHub Organizations"
    empty-message="There are no organizations."
    :item-count="gitHubApiStore.organizationList.length"
    :loading="gitHubApiStore.loading"
  >
    <list>
      <list-item
        v-for="item in gitHubApiStore.organizationList"
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
 * Allows for selecting a GitHub organization.
 */
export default {
  name: "GitHubOrganizationSelector",
};
</script>

<script setup lang="ts">
import { onMounted, watch } from "vue";
import { GitHubOrganizationSchema } from "@/types";
import { gitHubApiStore, integrationsStore } from "@/hooks";
import { StepperListStep, List, ListItem } from "@/components/common";

/**
 * Loads a user's GitHub organizations.
 */
async function handleReload() {
  if (!integrationsStore.validGitHubCredentials) return;

  await gitHubApiStore.handleLoadProjects();
}

/**
 * Handles a click to select an organization.
 * @param selectedOrganization - The organization to select.
 */
function handleOrganizationSelect(
  selectedOrganization: GitHubOrganizationSchema | undefined
) {
  integrationsStore.selectGitHubOrganization(selectedOrganization);
}

onMounted(() => handleReload());

watch(
  () => integrationsStore.validGitHubCredentials,
  () => handleReload()
);
</script>
