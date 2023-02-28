<template>
  <stepper-list-step
    title="GitHub Organizations"
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
 * Allows for selecting a GitHub organization.
 */
export default {
  name: "GitHubOrganizationSelector",
};
</script>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { GitHubOrganizationSchema } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleLoadGitHubProjects } from "@/api";
import { StepperListStep, List, ListItem } from "@/components/common";

const organizations = ref<GitHubOrganizationSchema[]>([]);
const loading = ref(false);

/**
 * Loads a user's GitHub organizations.
 */
async function handleReload() {
  if (!integrationsStore.validGitHubCredentials) return;

  integrationsStore.gitHubOrganization = undefined;
  loading.value = true;

  handleLoadGitHubProjects({
    onSuccess: (projects) => {
      organizations.value = [];

      projects.forEach(({ owner }) => {
        if (organizations.value.find(({ id }) => id === owner)) return;

        organizations.value.push({ id: owner, name: owner });
      });
    },
    onComplete: () => (loading.value = false),
  });
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
