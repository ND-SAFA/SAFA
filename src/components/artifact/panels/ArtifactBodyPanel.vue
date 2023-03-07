<template>
  <details-panel panel="displayArtifactBody">
    <artifact-body />
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays artifact content.
 */
export default {
  name: "ArtifactBodyPanel",
};
</script>

<script setup lang="ts">
import DetailsPanel from "@/components/navigation/detailsDrawer/DetailsPanel.vue";
import { ArtifactBody } from "../display";
</script>
