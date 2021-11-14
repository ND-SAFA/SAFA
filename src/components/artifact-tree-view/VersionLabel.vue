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
import Vue from "vue";
import { Project } from "@/types";
import { versionToString } from "@/util";
import { projectModule } from "@/store";

const DEFAULT_PROJECT_NAME = "Untitled";
const DEFAULT_VERSION_NAME = "X.X.X";

export default Vue.extend({
  name: "version-label",
  data() {
    return {
      projectName: DEFAULT_PROJECT_NAME,
      versionName: DEFAULT_VERSION_NAME,
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
  mounted() {
    this.setProjectName();
  },
  methods: {
    setProjectName() {
      const project = this.project;
      if (this.containsProject) {
        this.projectName = project.name;
        if (project.projectVersion !== undefined) {
          this.versionName = versionToString(project.projectVersion);
        }
      } else {
        this.projectName = DEFAULT_PROJECT_NAME;
        this.versionName = DEFAULT_VERSION_NAME;
      }
    },
  },
  watch: {
    project() {
      this.setProjectName();
    },
  },
});
</script>
