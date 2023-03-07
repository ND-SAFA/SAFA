<template>
  <details-panel panel="saveArtifact" data-cy="panel-artifact-save">
    <save-artifact />
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
import DetailsPanel from "@/components/navigation/detailsDrawer/DetailsPanel.vue";
import { SaveArtifact } from "../save";
</script>
