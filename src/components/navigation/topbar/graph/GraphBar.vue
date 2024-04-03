<template>
  <flex-box full-width justify="between" align="center" y="1">
    <flex-box align="center">
      <mode-buttons />
    </flex-box>
    <flex-box align="center">
      <update-button />
      <commit-buttons />
      <document-history />
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
import { DocumentHistory } from "@/components/document";
import ModeButtons from "./ModeButtons.vue";
import VisibleTypeButtons from "./VisibleTypeButtons.vue";
import UpdateButton from "./UpdateButton.vue";
</script>
