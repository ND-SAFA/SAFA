<template>
  <v-container>
    <h1 class="text-h4 my-2">Delta View</h1>
    <v-divider class="mb-2" />

    <v-btn
      v-if="!isDeltaViewEnabled"
      block
      large
      :disabled="!isProjectDefined"
      color="primary"
      @click="handleChange"
    >
      <v-icon class="pr-2">mdi-source-branch</v-icon>
      Compare Versions
    </v-btn>
    <v-btn
      v-else
      block
      large
      outlined
      :disabled="!isProjectDefined"
      @click="handleChange"
    >
      <v-icon class="pr-2">mdi-close</v-icon>
      Hide Delta View
    </v-btn>

    <delta-versions-modal
      v-if="isProjectDefined"
      :is-open="isModalOpen"
      :project="project"
      @close="isModalOpen = false"
      @submit="handleSubmit"
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { Project } from "@/types";
import { versionToString } from "@/util";
import { deltaModule, projectModule } from "@/store";
import DeltaVersionsModal from "./DeltaVersionsModal.vue";
import { handleReloadProject } from "@/api";

/**
 * Displays the delta panel navigation.
 */
export default Vue.extend({
  name: "DeltaPanelNav",
  components: {
    DeltaVersionsModal,
  },
  data: () => ({
    isModalOpen: false,
    errorMessage: undefined as string | undefined,
  }),
  computed: {
    /**
     * @return The current project.
     */
    project(): Project {
      return projectModule.getProject;
    },
    /**
     * @return Whether the current project is defined
     */
    isProjectDefined(): boolean {
      return this.project.projectId !== "";
    },
    /**
     * @return The delta after version.
     */
    afterVersion(): string {
      return versionToString(deltaModule.deltaVersion);
    },
    /**
     * @return The delta before version.
     */
    beforeVersion(): string {
      return versionToString(projectModule.getProject.projectVersion);
    },
    /**
     * @return Whether delta view is enabled.
     */
    isDeltaViewEnabled(): boolean {
      return deltaModule.inDeltaView;
    },
  },
  methods: {
    /**
     * Changes whether delta view is enabled.
     */
    handleChange(): void {
      if (!this.isDeltaViewEnabled) {
        this.isModalOpen = true;
      } else {
        deltaModule.setIsDeltaViewEnabled(false);
        handleReloadProject();
      }
    },
    /**
     * Enables delta view.
     */
    handleSubmit(): void {
      deltaModule.setIsDeltaViewEnabled(true);
    },
  },
  watch: {
    /**
     * Resets errors when the project changes.
     */
    project(): void {
      if (!this.isProjectDefined) return;

      this.errorMessage = undefined;
    },
  },
});
</script>
