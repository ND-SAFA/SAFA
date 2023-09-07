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
import { onMounted, watch } from "vue";
import { appStore, artifactSaveStore, selectionStore } from "@/hooks";
import { DetailsPanel, PanelCard, TextButton } from "@/components/common";
import { SaveArtifactInputs, SaveArtifactButtons } from "../save";

onMounted(() => {
  artifactSaveStore.resetArtifact(true);
});

watch(
  () => appStore.popups.detailsPanel && appStore.popups.saveArtifact,
  (openState) => {
    if (!openState) return;

    artifactSaveStore.resetArtifact(openState);
  }
);

watch(
  () => selectionStore.selectedArtifact,
  () => artifactSaveStore.resetArtifact(true)
);
</script>
