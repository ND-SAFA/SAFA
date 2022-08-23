<template>
  <v-container class="mt-2">
    <typography el="h1" variant="title" value="Delta View" />
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
import { handleReloadProject } from "@/api";
import { deltaStore, projectStore } from "@/hooks";
import DeltaVersionsModal from "./DeltaVersionsModal.vue";
import { Typography } from "@/components/common";

/**
 * Displays the delta panel navigation.
 */
export default Vue.extend({
  name: "DeltaPanelNav",
  components: {
    DeltaVersionsModal,
    Typography,
  },
  data: () => ({
    isModalOpen: false,
    errorMessage: undefined as string | undefined,
  }),
  computed: {
    /**
     * @return The current project.
     */
    project() {
      return projectStore.project;
    },
    /**
     * @return Whether the current project is defined
     */
    isProjectDefined(): boolean {
      return this.project.projectId !== "";
    },
    /**
     * @return Whether delta view is enabled.
     */
    isDeltaViewEnabled(): boolean {
      return deltaStore.inDeltaView;
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
        deltaStore.setIsDeltaViewEnabled(false);
        handleReloadProject();
      }
    },
    /**
     * Enables delta view.
     */
    handleSubmit(): void {
      deltaStore.setIsDeltaViewEnabled(true);
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
