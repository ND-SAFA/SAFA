<template>
  <v-container>
    <v-row justify="center">
      <label v-if="containsProject" text outlined color="primary">
        {{ projectName }}@{{ versionName }}
      </label>
      <label v-else text outlined color="primary"> No project selected. </label>
    </v-row>
  </v-container>
</template>
<script lang="ts">
import { Project } from "@/types/domain/project";
import { versionToString } from "@/util";
import Vue from "vue";
import { projectModule } from "@/store";
export default Vue.extend({
  name: "version-label",
  data() {
    return {
      projectName: "Unititled",
      versionName: "X.X.X",
    };
  },
  computed: {
    project(): Project {
      return projectModule.getProject;
    },
    containsProject(): boolean {
      return this.project.projectId !== "";
    },
  },
  watch: {
    project(project: Project) {
      this.projectName = project.name;
      if (project.projectVersion !== undefined) {
        this.versionName = versionToString(project.projectVersion);
      }
    },
  },
});
</script>
