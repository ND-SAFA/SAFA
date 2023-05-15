<template>
  <div>
    <text-button
      text
      label="View Artifact"
      b="2"
      icon="artifact"
      @click="handleViewArtifact"
    />
    <panel-card>
      <typography
        default-expanded
        :collapse-length="0"
        :variant="variant"
        el="p"
        :value="body"
      />
    </panel-card>
  </div>
</template>

<script lang="ts">
/**
 * Displays the selected node's body.
 */
export default {
  name: "ArtifactBody",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { isCodeArtifact } from "@/util";
import { appStore, selectionStore } from "@/hooks";
import { Typography, TextButton, PanelCard } from "@/components/common";

const artifact = computed(() => selectionStore.selectedArtifact);

const body = computed(() => artifact.value?.body.trim() || "");

const variant = computed(() =>
  isCodeArtifact(artifact.value?.name || "") ? "code" : "expandable"
);

/**
 * Displays the entire artifact.
 */
function handleViewArtifact(): void {
  appStore.openDetailsPanel("displayArtifact");
}
</script>
