<template>
  <flex-box full-width justify="between" align="center" y="1">
    <flex-box align="center">
      <document-selector />
      <mode-buttons />
    </flex-box>
    <flex-box align="center">
      <visible-type-buttons v-if="!smallWindow" />
      <graph-buttons v-if="!smallWindow" />
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
import { useScreen } from "@/hooks";
import { FlexBox, CommitButtons } from "@/components/common";
import { DocumentSelector } from "@/components/document";
import GraphButtons from "./GraphButtons.vue";
import ModeButtons from "./ModeButtons.vue";
import VisibleTypeButtons from "./VisibleTypeButtons.vue";

const { smallWindow } = useScreen();
</script>
