<template>
  <flex-box full-width justify="between" align="center" y="1">
    <flex-box align="center">
      <document-selector />
      <mode-buttons />
    </flex-box>
    <flex-box align="center">
      <graph-buttons />
      <separator vertical inset nav x="1" />
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
import { FlexBox, CommitButtons, Separator } from "@/components/common";
import { DocumentSelector } from "@/components/document";
import GraphButtons from "./GraphButtons.vue";
import ModeButtons from "./ModeButtons.vue";
</script>
