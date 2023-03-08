<template>
  <details-panel panel="displayArtifact">
    <artifact-buttons />
    <artifact-content />
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays artifact information.
 */
export default {
  name: "ArtifactPanel",
};
</script>

<script setup lang="ts">
import DetailsPanel from "@/components/navigation/detailsDrawer/DetailsPanel.vue";
import { ArtifactButtons, ArtifactContent } from "../display";
</script>
