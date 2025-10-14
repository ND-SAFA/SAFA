<template>
  <div v-if="displayPopup" class="cy-popup full-height full-width">
    <div class="q-mx-auto width-fit q-pa-md text-center">
      <panel-card
        v-if="projectStore.isProjectDefined"
        title="Welcome to SAFA!"
        subtitle="Create an artifact to get started."
      >
        <text-button
          text
          icon="add"
          label="Create Artifact"
          @click="appStore.openDetailsPanel('saveArtifact')"
        />
      </panel-card>
      <panel-card
        v-else
        title="Welcome to SAFA!"
        subtitle="Create a project to get started."
      >
        <text-button
          text
          icon="add"
          label="Create Project"
          @click="navigateTo(Routes.PROJECT_CREATOR)"
        />
      </panel-card>
    </div>
  </div>
</template>

<script lang="ts">
/**
 * Renders options for creating a project or artifact when the graph is empty.
 */
export default {
  name: "EmptyGraphButtons",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore, timStore, projectStore } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import { PanelCard, TextButton } from "@/components/common";

const displayPopup = computed(
  () => !appStore.isLoading && timStore.artifactTypes.length === 0
);
</script>
