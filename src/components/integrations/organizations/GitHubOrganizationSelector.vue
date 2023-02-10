<template>
  <stepper-list-step
    title="GitHub Organizations"
    :item-count="organizations.length"
    :loading="organizationsLoading"
    empty-message="There are no organizations."
  >
    <template v-for="organization in organizations" :key="organization.id">
      <v-list-item three-line @click="handleOrganizationSelect(organization)">
        <v-list-item-title v-text="organization.name" />
      </v-list-item>
    </template>
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
import { ref, watch } from "vue";
import { GitHubOrganizationSchema } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleLoadGitHubProjects } from "@/api";
import { StepperListStep } from "@/components/common";

const organizations = ref<GitHubOrganizationSchema[]>([]);
const organizationsLoading = ref(false);

/**
 * Loads a user's GitHub organizations.
 */
async function loadOrganizations() {
  if (!integrationsStore.validGitHubCredentials) return;

  integrationsStore.gitHubOrganization = undefined;
  organizationsLoading.value = true;

  handleLoadGitHubProjects({
    onSuccess: (projects) => {
      organizations.value = [];

      projects.forEach(({ owner }) => {
        if (organizations.value.find(({ id }) => id === owner)) return;

        organizations.value.push({ id: owner, name: owner });
      });

      organizationsLoading.value = false;
    },
    onError: () => (organizationsLoading.value = false),
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

watch(
  () => integrationsStore.validGitHubCredentials,
  () => loadOrganizations()
);
</script>
