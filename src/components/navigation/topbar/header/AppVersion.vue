<template>
  <flex-box align="center">
    <typography
      el="h1"
      variant="subtitle"
      color="accent"
      style="white-space: nowrap"
      :value="projectName"
      x="4"
    />
    <v-select
      v-if="isProjectDefined"
      outlined
      hide-details
      dark
      dense
      label="Version"
      :value="versionName"
      :items="[versionName]"
      style="width: 100px"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { versionToString } from "@/util";
import { projectStore } from "@/hooks";
import { Typography, FlexBox } from "@/components/common";

/**
 * Displays the current project version.
 */
export default Vue.extend({
  name: "AppVersion",
  components: { FlexBox, Typography },
  computed: {
    /**
     * @return The current project.
     */
    project() {
      return projectStore.project;
    },
    /**
     * @return Whether a project is currently loaded.
     */
    isProjectDefined(): boolean {
      return projectStore.isProjectDefined;
    },
    /**
     * @return The name of this project.
     */
    projectName(): string {
      return this.isProjectDefined ? this.project.name : "No Project Selected";
    },
    /**
     * @return The name of this version.
     */
    versionName(): string {
      return this.isProjectDefined
        ? versionToString(this.project.projectVersion)
        : "";
    },
  },
});
</script>
