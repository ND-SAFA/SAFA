<template>
  <flex-box full-width justify="between" align="center" y="1">
    <flex-box align="center">
      <document-selector />
      <mode-buttons />
    </flex-box>
    <flex-box align="center">
      <graph-buttons />
      <q-separator vertical inset color="accent" class="faded q-mx-sm" />
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
