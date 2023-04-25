<template>
  <stepper-list-step
    title="GitHub Repositories"
    empty-message="There are no repositories."
    :item-count="projects.length"
  >
    <list>
      <list-item
        v-for="item in projects"
        :key="item.name"
        :title="item.name"
        :subtitle="getRepositoryTime(item)"
        clickable
        :active="projectName === item.name"
        active-class="bg-background"
        @click="handleProjectSelect(item)"
      />
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
import { StepperListStep, List, ListItem } from "@/components/common";

const projects = ref<GitHubProjectSchema[]>([]);

const organizationName = computed(
  () => integrationsStore.gitHubOrganization?.name
);

const projectName = computed(() => integrationsStore.gitHubProject?.name);

/**
 * Loads a user's GitHub projects for a selected organization.
 */
function handleReload() {
  if (!integrationsStore.gitHubOrganization) return;

  integrationsStore.gitHubProject = undefined;

  projects.value = integrationsStore.gitHubProjectList.filter(
    ({ owner }) => owner === organizationName.value
  );
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
