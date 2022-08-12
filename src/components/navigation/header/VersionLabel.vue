<template>
  <typography
    el="h1"
    variant="subtitle"
    color="white"
    classes="width-max"
    :value="versionDisplayName"
  />
</template>

<script lang="ts">
import Vue from "vue";
import { versionToString } from "@/util";
import { projectModule } from "@/store";
import { Typography } from "@/components/common";

const DEFAULT_PROJECT_NAME = "Untitled";
const DEFAULT_VERSION_NAME = "X.X.X";

/**
 * Displays the current project version.
 */
export default Vue.extend({
  name: "VersionLabel",
  components: { Typography },
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
      return this.projectExists
        ? `${this.projectName}@${this.versionName}`
        : "No Project Selected";
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
