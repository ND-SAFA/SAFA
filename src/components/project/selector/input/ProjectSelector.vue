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
        @click="identifierSaveStore.selectIdentifier(undefined, 'save')"
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
import { getProjectApiStore, identifierSaveStore, useTheme } from "@/hooks";
import { TextButton } from "@/components/common";

const { darkMode } = useTheme();
</script>
