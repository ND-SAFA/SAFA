<template>
  <stepper-list-step
    title="GitHub Repositories"
    empty-message="There are no repositories."
    :item-count="projects.length"
    :loading="loading"
  >
    <list :items="projects">
      <template #item="{ item }">
        <list-item
          :title="item.name"
          :subtitle="getRepositoryTime(item)"
          @click="handleProjectSelect(item)"
        />
      </template>
    </list>
  </stepper-list-step>
</template>

<script lang="ts">
/**
 * Allows for selecting a GitHub repository.
 */
export default {
  name: "GitHubProjectSelector",
};
</script>

<script setup lang="ts">
import { computed, ref, onMounted, watch } from "vue";
import { GitHubProjectSchema } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleLoadGitHubProjects } from "@/api";
import { StepperListStep, List, ListItem } from "@/components/common";

const projects = ref<GitHubProjectSchema[]>([]);
const loading = ref(false);

const organizationName = computed(
  () => integrationsStore.gitHubOrganization?.name
);

/**
 * Loads a user's GitHub projects for a selected organization.
 */
function handleReload() {
  if (!integrationsStore.gitHubOrganization) return;

  integrationsStore.gitHubProject = undefined;
  loading.value = true;

  handleLoadGitHubProjects({
    onSuccess: (repositories) => {
      projects.value = repositories.filter(
        ({ owner }) => owner === organizationName.value
      );
    },
    onComplete: () => (loading.value = false),
  });
}

/**
 * Returns a repository's last updated time.
 * @param repository - The repository to extract from.
 * @return The last updated time.
 */
function getRepositoryTime(repository: GitHubProjectSchema): string {
  const updated = new Date(repository.created_at);

  return `Created on ${updated.getMonth()}/${updated.getDate()}/${updated.getFullYear()}`;
}

/**
 * SHandles a click to select a repository.
 * @param project - The repository to select.
 */
function handleProjectSelect(project: GitHubProjectSchema | undefined) {
  integrationsStore.selectGitHubProject(project);
}

onMounted(() => handleReload());

watch(
  () => organizationName.value,
  () => handleReload()
);
</script>
