<template>
  <stepper-list-step
    title="Jira Projects"
    empty-message="There are no projects."
    :item-count="projects.length"
    :loading="loading"
  >
    <list>
      <list-item
        v-for="item in projects"
        :key="item.name"
        :title="item.name"
        :subtitle="item.key"
        @click="handleProjectSelect(item)"
      >
        <template #icon>
          <img :src="item.mediumAvatarUrl" :alt="item.name" />
        </template>
      </list-item>
    </list>
  </stepper-list-step>
</template>

<script lang="ts">
/**
 * Allows for selecting a jira project.
 */
export default {
  name: "JiraProjectSelector",
};
</script>

<script setup lang="ts">
import { onMounted, watch, ref } from "vue";
import { JiraProjectSchema } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleLoadJiraProjects } from "@/api";
import { StepperListStep, List, ListItem } from "@/components/common";

const projects = ref<JiraProjectSchema[]>([]);
const loading = ref(false);

/**
 * Loads a user's Jira projects for a selected site.
 */
function handleReload() {
  if (!integrationsStore.jiraOrganization) return;

  integrationsStore.jiraProject = undefined;
  loading.value = true;

  handleLoadJiraProjects({
    onSuccess: (jiraProjects) => {
      projects.value = jiraProjects;
    },
    onComplete: () => (loading.value = false),
  });
}

/**
 * Handles a click to select a project.
 * @param project - The project to select.
 */
function handleProjectSelect(project: JiraProjectSchema | undefined) {
  integrationsStore.selectJiraProject(project);
}

onMounted(() => handleReload());

watch(
  () => integrationsStore.jiraOrganization,
  () => handleReload()
);
</script>
