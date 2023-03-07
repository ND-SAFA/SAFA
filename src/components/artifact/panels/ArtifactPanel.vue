<template>
  <div v-if="isOpen">
    <artifact-buttons />
    <artifact-content />
  </div>
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
import { computed } from "vue";
import { appStore } from "@/hooks";
import { ArtifactButtons, ArtifactContent } from "../display";

const isOpen = computed(
  () => appStore.isDetailsPanelOpen === "displayArtifact"
);
</script>
