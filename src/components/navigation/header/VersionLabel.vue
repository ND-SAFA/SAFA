<template>
  <v-row justify="end">
    <h1 v-if="projectExists" class="text-h5 white--text">
      {{ versionDisplayName }}
    </h1>
    <h1 v-else class="text-h5 white--text">No Project Selected</h1>
  </v-row>
</template>
<script lang="ts">
import Vue from "vue";
import { versionToString } from "@/util";
import { projectModule } from "@/store";

const DEFAULT_PROJECT_NAME = "Untitled";
const DEFAULT_VERSION_NAME = "X.X.X";

/**
 * Displays the current project version.
 */
export default Vue.extend({
  name: "VersionLabel",
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
    /**
     * @return The name of this project and version.
     */
    versionDisplayName(): string {
      return `${this.projectName}@${this.versionName}`;
    },
    /**
     * @return The current project.
     */
    project() {
      return projectModule.getProject;
    },
    /**
     * @return Whether there is currently a project loaded.
     */
    projectExists(): boolean {
      return projectModule.isProjectDefined;
    },
  },
  methods: {
    /**
     * Updates the project name.
     */
    setProjectName() {
      const { name, projectVersion, projectId } = projectModule.getProject;

      if (projectId) {
        this.projectName = name;

        if (!projectVersion) return;

        this.versionName = versionToString(projectVersion);
      } else {
        this.projectName = DEFAULT_PROJECT_NAME;
        this.versionName = DEFAULT_VERSION_NAME;
      }
    },
  },
  watch: {
    /**
     * Updates the project name when the project changes.
     */
    project() {
      this.setProjectName();
    },
  },
});
</script>
