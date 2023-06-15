<template>
  <q-select
    v-model="project"
    outlined
    dark
    :options-dark="darkMode"
    label="Project"
    :options="projects"
    option-value="projectId"
    option-label="name"
    class="nav-input"
    color="primary"
  >
    <template #after-options>
      <text-button
        text
        block
        label="Add Project"
        icon="add"
        @click="openCreateProject = true"
      />
    </template>
    <template #append>
      <project-identifier-modal
        :open="openCreateProject"
        @close="openCreateProject = false"
        @save="handleProjectCreated"
      />
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 Displays the current project, and allows it to be changed.
 */
export default {
  name: "ProjectSelector",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { IdentifierSchema } from "@/types";
import { getVersionApiStore, projectStore, useTheme } from "@/hooks";
import { handleGetProjects } from "@/api";
import { TextButton } from "@/components/common";
import { ProjectIdentifierModal } from "../../base";

const openCreateProject = ref(false);

const { darkMode } = useTheme();

const projects = computed(() => projectStore.allProjects);

const project = computed({
  get: () => (projectStore.projectId ? projectStore.project : undefined),
  set(identifier: IdentifierSchema | undefined) {
    if (!identifier) return;

    getVersionApiStore.handleLoadCurrentVersion(identifier);
  },
});

/**
 * Reloads projects when a new one is created.
 */
async function handleProjectCreated(): Promise<void> {
  await handleGetProjects({});
}

onMounted(() => handleGetProjects({}));
</script>
