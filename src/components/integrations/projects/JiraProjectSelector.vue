<template>
  <stepper-list-step
    title="Jira Projects"
    empty-message="There are no projects."
    :item-count="jiraApiStore.projectList.length"
    :loading="jiraApiStore.loading"
  >
    <list>
      <list-item
        v-for="item in jiraApiStore.projectList"
        :key="item.name"
        :title="item.name"
        :subtitle="item.key"
        clickable
        :active="projectName === item.name"
        active-class="bg-background"
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
import { onMounted, watch, computed } from "vue";
import { JiraProjectSchema } from "@/types";
import { integrationsStore, jiraApiStore } from "@/hooks";
import { StepperListStep, List, ListItem } from "@/components/common";

const projectName = computed(() => integrationsStore.jiraProject?.name);

/**
 * Loads a user's Jira projects for a selected site.
 */
function handleReload() {
  if (!integrationsStore.jiraOrganization) return;

  jiraApiStore.handleLoadProjects();
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
