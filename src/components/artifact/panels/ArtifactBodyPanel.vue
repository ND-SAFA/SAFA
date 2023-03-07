<template>
  <div v-if="isOpen">
    <artifact-body />
  </div>
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
import { computed } from "vue";
import { appStore } from "@/hooks";
import { ArtifactBody } from "../display";

const isOpen = computed(
  () => appStore.isDetailsPanelOpen === "displayArtifactBody"
);
</script>
