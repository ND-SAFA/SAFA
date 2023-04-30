<template>
  <q-select
    v-if="project.projectId"
    v-model="project"
    dense
    outlined
    dark
    :options-dark="darkMode"
    options-selected-class="primary"
    label="Project"
    :options="projects"
    option-value="projectId"
    option-label="name"
    class="nav-input"
    color="accent"
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
  <typography v-else variant="subtitle" value="No Project Selected" />
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
import { projectStore, useTheme } from "@/hooks";
import {
  getProjectVersions,
  handleLoadVersion,
  handleGetProjects,
} from "@/api";
import { TextButton, Typography } from "@/components/common";
import { ProjectIdentifierModal } from "../base";

const openCreateProject = ref(false);

const { darkMode } = useTheme();

const projects = computed(() => projectStore.allProjects);

const project = computed({
  get: () => projectStore.project,
  set(identifier: IdentifierSchema | undefined) {
    if (!identifier) return;

    getProjectVersions(identifier.projectId).then((versions) => {
      handleLoadVersion(versions[0].versionId);
    });
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
