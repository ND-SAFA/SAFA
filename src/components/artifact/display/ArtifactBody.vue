<template>
  <div>
    <text-button
      text
      label="View Artifact"
      b="2"
      icon="artifact"
      @click="appStore.openDetailsPanel('displayArtifact')"
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
import { appStore, artifactStore } from "@/hooks";
import { Typography, TextButton, PanelCard } from "@/components/common";

const artifact = computed(() => artifactStore.selectedArtifact);

const body = computed(() => artifact.value?.body.trim() || "");

const variant = computed(() =>
  artifact.value?.isCode ? "code" : "expandable"
);
</script>
