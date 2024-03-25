<template>
  <details-panel panel="saveArtifact" data-cy="panel-artifact-save">
    <text-button
      text
      label="View Artifact"
      b="2"
      icon="artifact"
      @click="appStore.openDetailsPanel('displayArtifact')"
    />
    <panel-card>
      <save-artifact-inputs />
      <template #actions>
        <save-artifact-buttons />
      </template>
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Allows for creating and editing artifacts.
 */
export default {
  name: "SaveArtifactPanel",
};
</script>

<script setup lang="ts">
import { watch } from "vue";
import { appStore, artifactSaveStore, artifactStore } from "@/hooks";
import { DetailsPanel, PanelCard, TextButton } from "@/components/common";
import {
  SaveArtifactInputs,
  SaveArtifactButtons,
} from "@/components/artifact/save";

watch(
  () => artifactStore.selectedArtifact,
  () => artifactSaveStore.resetArtifact()
);
</script>
