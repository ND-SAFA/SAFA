<template>
  <flex-box full-width justify="between" align="center" y="1">
    <mode-buttons />
    <flex-box align="center">
      <commit-buttons />
      <graph-buttons />
      <visible-type-buttons />
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
import GraphButtons from "./GraphButtons.vue";
import ModeButtons from "./ModeButtons.vue";
import VisibleTypeButtons from "./VisibleTypeButtons.vue";
</script>
