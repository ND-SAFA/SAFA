<template>
  <v-row justify="end">
    <h1 v-if="projectExists" class="text-h5 white--text">
      {{ projectName }}@{{ versionName }}
    </h1>
    <h1 v-else class="text-h5 white--text">No Project Selected</h1>
  </v-row>
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
  mounted() {
    this.setProjectName();
  },
  computed: {
    project(): Project {
      return projectModule.getProject;
    },
  },
  methods: {
    projectExists(): boolean {
      return projectModule.isProjectDefined;
    },
    setProjectName() {
      const { name, projectVersion, projectId } = projectModule.getProject;

      if (projectId) {
        this.projectName = name;
        if (projectVersion !== undefined) {
          this.versionName = versionToString(projectVersion);
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
