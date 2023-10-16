<template>
  <flex-box full-width justify="between" align="center" y="1">
    <flex-box align="center">
      <document-selector v-if="!ENABLED_FEATURES.NAV_BREADCRUMBS" />
      <mode-buttons />
    </flex-box>
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
import { ENABLED_FEATURES } from "@/util";
import { FlexBox, CommitButtons } from "@/components/common";
import { DocumentSelector } from "@/components/document";
import GraphButtons from "./GraphButtons.vue";
import ModeButtons from "./ModeButtons.vue";
import VisibleTypeButtons from "./VisibleTypeButtons.vue";
</script>
