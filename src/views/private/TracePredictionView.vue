<template>
  <private-page full-window>
    <trace-prediction-tabs />
  </private-page>
</template>

<script lang="ts">
/**
 * Renders a page for model training and trace approval.
 */
export default {
  name: "ApproveLinksView",
};
</script>

<script setup lang="ts">
import { PrivatePage, TracePredictionTabs } from "@/components";
</script>
