<template>
  <q-select
    v-model="getProjectApiStore.currentProject"
    outlined
    dark
    :options-dark="darkMode"
    label="Project"
    :options="getProjectApiStore.allProjects"
    option-value="projectId"
    option-label="name"
    class="nav-input"
    color="primary"
    @popup-show="getProjectApiStore.handleReload()"
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
import { ref } from "vue";
import { getProjectApiStore, useTheme } from "@/hooks";
import { TextButton } from "@/components/common";
import { ProjectIdentifierModal } from "../../base";

const openCreateProject = ref(false);

const { darkMode } = useTheme();

/**
 * Reloads projects when a new one is created.
 */
async function handleProjectCreated(): Promise<void> {
  await getProjectApiStore.handleReload();
}
</script>
