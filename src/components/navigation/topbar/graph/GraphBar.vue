<template>
  <flex-box full-width justify="space-between" align="center" r="1">
    <flex-box align="center">
      <document-selector />
      <mode-buttons />
    </flex-box>
    <flex-box align="center">
      <graph-buttons />
      <v-divider inset vertical class="text-accent mx-1 mb-2" />
      <commit-buttons />
    </flex-box>
  </flex-box>
</template>

<script lang="ts">
/**
 * Renders options specific to the artifact graph.
 */
export default {
  name: "GraphBar",
};
</script>

<script setup lang="ts">
import { FlexBox, CommitButtons } from "@/components/common";
import { DocumentSelector } from "@/components/document";
import GraphButtons from "./GraphButtons.vue";
import ModeButtons from "./ModeButtons.vue";
</script>
