<template>
  <typography
    el="h1"
    variant="subtitle"
    color="accent"
    style="white-space: nowrap"
    x="2"
    :value="versionDisplayName"
  />
</template>

<script lang="ts">
import Vue from "vue";
import { versionToString } from "@/util";
import { projectStore } from "@/hooks";
import { Typography } from "@/components/common";

/**
 * Displays the current project version.
 */
export default Vue.extend({
  name: "AppVersion",
  components: { Typography },
  computed: {
    /**
     * @return The current project.
     */
    project() {
      return projectStore.project;
    },
    /**
     * @return The name of this project and version.
     */
    versionDisplayName(): string {
      const { name, projectVersion } = projectStore.project;

      return projectStore.isProjectDefined
        ? `${name}@${versionToString(projectVersion)}`
        : "No Project Selected";
    },
  },
});
</script>
