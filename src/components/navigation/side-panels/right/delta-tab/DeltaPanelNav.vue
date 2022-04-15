<template>
  <v-container>
    <h1 class="text-h4 my-2">Delta View</h1>
    <v-row justify="center">
      <v-switch
        color="primary"
        @click="handleChange"
        :value="isDeltaViewEnabled"
        :error-messages="errorMessage"
        readonly
      >
        <template v-slot:label> Enable Delta View Mode </template>
      </v-switch>
    </v-row>
    <v-row justify="center" v-if="isDeltaViewEnabled">
      <v-btn
        v-if="isProjectDefined"
        color="primary"
        @click="isModalOpen = true"
        class="pt-6 pb-6"
      >
        <v-icon class="pr-2">mdi-source-branch</v-icon>
        Compare Against <br />
        {{ afterVersion }}
      </v-btn>
      <p v-else>No project has been selected.</p>
    </v-row>
    <delta-versions-modal
      v-if="isProjectDefined"
      :is-open="isModalOpen"
      :project="project"
      @close="isModalOpen = false"
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
        if (this.isProjectDefined) {
          deltaModule.setIsDeltaViewEnabled(true);
          this.isModalOpen = true;
        } else {
          this.errorMessage = "Please select a baseline project version";
        }
      } else {
        deltaModule.setIsDeltaViewEnabled(false);
        handleReloadProject();
      }
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
