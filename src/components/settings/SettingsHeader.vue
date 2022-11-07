<template>
  <div>
    <typography el="h1" variant="title" :value="project.name" />
    <v-divider class="mb-2" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { projectStore } from "@/hooks";
import { Typography } from "@/components/common";

/**
 * Represents the section describing the project name and descriptions
 * within the settings.
 */
export default Vue.extend({
  name: "SettingsHeader",
  components: {
    Typography,
  },
  computed: {
    /**
     * @return The current project.
     */
    project() {
      return projectStore.project;
    },
  },
});
</script>
